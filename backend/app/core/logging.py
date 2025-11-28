"""
Конфигурация логирования для FastAPI приложения.

Этот модуль настраивает структурированное логирование в стиле FastAPI.
Использует стандартный модуль logging Python с настройкой форматирования
и уровней логирования в зависимости от окружения.
"""

import logging
import sys
from typing import Any

from app.core.settings import settings


def setup_logging() -> None:
    """
    Настраивает логирование для всего приложения.

    В зависимости от окружения (local/staging/production) устанавливает
    разные уровни логирования и форматы:
    - local: DEBUG уровень, цветной вывод в консоль
    - staging/production: INFO уровень, структурированный формат
    """
    # Определяем уровень логирования в зависимости от окружения
    if settings.ENVIRONMENT == "local":
        log_level = logging.DEBUG
        log_format = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s"
    else:
        log_level = logging.INFO
        log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

    # Настраиваем базовый логгер
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,  # Перезаписываем существующую конфигурацию
    )

    # Настраиваем уровни для сторонних библиотек
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING if settings.ENVIRONMENT != "local" else logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.WARNING if settings.ENVIRONMENT != "local" else logging.INFO
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Получаем логгер для нашего приложения
    logger = logging.getLogger("app")
    logger.setLevel(log_level)

    logger.info(
        f"Logging configured for environment: {settings.ENVIRONMENT}",
        extra={"environment": settings.ENVIRONMENT, "log_level": logging.getLevelName(log_level)},
    )


def get_logger(name: str) -> logging.Logger:
    """
    Получить логгер с указанным именем.

    Args:
        name: Имя логгера (обычно __name__ модуля)

    Returns:
        Настроенный логгер

    Example:
        ```python
        from app.core.logging import get_logger

        logger = get_logger(__name__)
        logger.info("Application started")
        ```
    """
    return logging.getLogger(f"app.{name}")


class LoggingMiddleware:
    """
    Middleware для логирования HTTP запросов в стиле FastAPI.

    Использует BaseHTTPMiddleware для перехвата всех HTTP запросов
    и логирования информации о них: метод, путь, статус код, время выполнения.

    Example:
        ```python
        from app.core.logging import LoggingMiddleware

        app.add_middleware(LoggingMiddleware)
        ```
    """

    def __init__(self, app: Any):
        from starlette.middleware.base import BaseHTTPMiddleware

        self.app = app
        self.logger = get_logger("requests")

    async def __call__(self, scope: dict, receive: Any, send: Any) -> None:
        import time

        from starlette.requests import Request

        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = time.time()
        request = Request(scope, receive)
        method = request.method
        path = request.url.path
        client_ip = request.client.host if request.client else "unknown"

        # Логируем начало запроса (только в DEBUG режиме)
        self.logger.debug(
            f"Request started: {method} {path}",
            extra={
                "method": method,
                "path": path,
                "client_ip": client_ip,
            },
        )

        # Обрабатываем запрос
        status_code = 200

        async def send_wrapper(message: dict) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as e:
            status_code = 500
            self.logger.error(
                f"Request failed: {method} {path}",
                exc_info=True,
                extra={
                    "method": method,
                    "path": path,
                    "status_code": status_code,
                    "error": str(e),
                },
            )
            raise
        finally:
            # Логируем завершение запроса
            duration = time.time() - start_time
            log_level = logging.INFO if status_code < 400 else logging.WARNING
            self.logger.log(
                log_level,
                f"{method} {path} - {status_code} ({duration:.3f}s)",
                extra={
                    "method": method,
                    "path": path,
                    "status_code": status_code,
                    "duration": duration,
                    "client_ip": client_ip,
                },
            )
