from fastapi import APIRouter, Query, Depends
from typing import Annotated

from sqlalchemy.orm import Session

from app.dependency import get_db
from app.service import wallets as wallets_service
from app.schemas import CreateWalletRequests

router = APIRouter()

@router.get('/balance') # ручка для получения баланса кошелька
async def get_balance(wallet_name: Annotated[str | None, Query()] = None, db: Session = Depends(get_db)):
    return wallets_service.get_balance(db, wallet_name)

@router.post('/wallets/') # ручка для создания кошелька
async def create_wallet(wallet: CreateWalletRequests, db: Session = Depends(get_db)):
    return wallets_service.create_wallet(db, wallet)

