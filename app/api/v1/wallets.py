from fastapi import APIRouter, Query
from typing import Annotated

from app.service import wallets as wallets_service
from app.schemas import CreateWalletRequests

router = APIRouter()

@router.get('/balance') # ручка для получения баланса кошелька
async def get_balance(wallet_name: Annotated[str | None, Query()] = None):
    return wallets_service.get_balance(wallet_name)

@router.post('/wallets/') # ручка для создания кошелька
async def create_wallet(wallet: CreateWalletRequests):
    return wallets_service.create_wallet(wallet)

