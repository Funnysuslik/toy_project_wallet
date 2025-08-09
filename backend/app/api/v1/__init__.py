# This file makes the v1 directory a Python package
from fastapi import APIRouter

from app.api.v1.users import users_router
from app.api.v1.transactions import transactions_router
from app.api.v1.wallets import wallets_router

main_router = APIRouter()

main_router.include_router(users_router)
main_router.include_router(transactions_router)
main_router.include_router(wallets_router)