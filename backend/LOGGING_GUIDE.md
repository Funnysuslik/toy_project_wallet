# Руководство по логированию в FastAPI

Это руководство объясняет, как использовать логирование в бэкенде в стиле FastAPI.

## Быстрый старт

### 1. Импорт и инициализация логгера

В любом модуле вашего приложения:

```python
from app.core.logging import get_logger

# Создаем логгер для текущего модуля
logger = get_logger(__name__)
```

### 2. Использование в эндпоинтах

```python
from fastapi import APIRouter
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.get("/items/{item_id}")
async def get_item(item_id: int):
    logger.info(f"Fetching item with id: {item_id}")

    try:
        # Ваша логика
        item = await fetch_item(item_id)
        logger.debug(f"Item found: {item}")
        return item
    except ItemNotFound:
        logger.warning(f"Item {item_id} not found")
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        logger.error(f"Error fetching item {item_id}", exc_info=True)
        raise
```

## Уровни логирования

### DEBUG
Для детальной отладочной информации:
```python
logger.debug("Detailed debug information")
logger.debug(f"Variable value: {variable}")
```

### INFO
Для информационных сообщений о нормальной работе:
```python
logger.info("User logged in successfully")
logger.info(f"Processing request for user: {user_id}")
```

### WARNING
Для предупреждений о потенциальных проблемах:
```python
logger.warning("Rate limit approaching")
logger.warning(f"User {user_id} attempted unauthorized action")
```

### ERROR
Для ошибок, которые не останавливают работу приложения:
```python
logger.error("Failed to send email", exc_info=True)
logger.error(f"Database query failed: {error}")
```

### CRITICAL
Для критических ошибок, требующих немедленного внимания:
```python
logger.critical("Database connection lost")
logger.critical("Payment processing failed", exc_info=True)
```

## Примеры использования

### Логирование в эндпоинтах

```python
from app.core.logging import get_logger
from fastapi import APIRouter, HTTPException

router = APIRouter()
logger = get_logger(__name__)

@router.post("/users")
async def create_user(user_data: UserCreate):
    logger.info(f"Creating user with email: {user_data.email}")

    # Проверка существования пользователя
    existing_user = await get_user_by_email(user_data.email)
    if existing_user:
        logger.warning(f"User creation failed: email {user_data.email} already exists")
        raise HTTPException(status_code=400, detail="Email already registered")

    # Создание пользователя
    try:
        new_user = await create_user(user_data)
        logger.info(f"User created successfully: {new_user.id}")
        return new_user
    except Exception as e:
        logger.error(f"Error creating user: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
```

### Логирование с контекстом

```python
@router.get("/transactions")
async def get_transactions(user: CurrentUser, skip: int = 0, limit: int = 100):
    logger.info(
        f"Fetching transactions for user {user.id}",
        extra={
            "user_id": user.id,
            "skip": skip,
            "limit": limit
        }
    )

    transactions = await get_user_transactions(user.id, skip, limit)
    logger.debug(f"Found {len(transactions)} transactions")

    return transactions
```

### Логирование ошибок с трассировкой

```python
try:
    result = await complex_operation()
except SpecificException as e:
    logger.error(
        f"Specific error occurred: {e}",
        exc_info=True,  # Включает полный traceback
        extra={"operation": "complex_operation", "user_id": user.id}
    )
    raise
```

## Настройка логирования

### Уровни логирования по окружениям

- **local**: DEBUG - детальная информация для разработки
- **staging**: INFO - общая информация о работе
- **production**: INFO - только важная информация

### Настройка в settings.py

```python
# В .env файле можно задать:
LOG_LEVEL=DEBUG  # или INFO, WARNING, ERROR, CRITICAL
ENVIRONMENT=local  # или staging, production
```

## Логирование запросов

Логирование HTTP запросов уже настроено автоматически через uvicorn.
В режиме `local` вы увидите все запросы, в других режимах - только ошибки.

## Лучшие практики

1. **Используйте правильные уровни**:
   - DEBUG для отладки
   - INFO для важных событий
   - WARNING для потенциальных проблем
   - ERROR для ошибок
   - CRITICAL для критических ситуаций

2. **Добавляйте контекст**:
   ```python
   logger.info(f"User {user_id} performed action", extra={"user_id": user_id, "action": "login"})
   ```

3. **Логируйте исключения с exc_info=True**:
   ```python
   except Exception as e:
       logger.error("Operation failed", exc_info=True)
   ```

4. **Не логируйте чувствительные данные**:
   ```python
   # ❌ Плохо
   logger.info(f"User password: {password}")

   # ✅ Хорошо
   logger.info(f"User {user_id} changed password")
   ```

5. **Используйте структурированное логирование**:
   ```python
   logger.info(
       "Transaction created",
       extra={
           "transaction_id": transaction.id,
           "amount": transaction.amount,
           "user_id": transaction.user_id
       }
   )
   ```

## Примеры из проекта

Смотрите файл `app/api/v1/users.py` для примеров использования логирования в реальных эндпоинтах.
