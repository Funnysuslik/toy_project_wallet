# This file makes the v1 directory a Python package
from fastapi import APIRouter

from .users import users_router
from .transactions import transactions_router
from .wallets import wallets_router

main_router = APIRouter()

main_router.include_router(users_router)
main_router.include_router(transactions_router)
main_router.include_router(wallets_router)