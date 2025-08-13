# This file makes the v1 directory a Python package
from fastapi import APIRouter

from app.core.settings import settings
from .users import users_router
from .transactions import transactions_router
from .wallets import wallets_router

main_router = APIRouter(prefix=settings.API_V1_STR)

main_router.include_router(users_router)
main_router.include_router(transactions_router)
main_router.include_router(wallets_router)
