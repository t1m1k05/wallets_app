from fastapi import APIRouter, Query, Depends
from typing import Annotated

from sqlalchemy.orm import Session

from app.api.v1.users import get_current_user
from app.dependency import get_db
from app.models import User
from app.service import wallets as wallets_service
from app.schemas import CreateWalletRequests, WalletResponse

router = APIRouter()

@router.get('/balance') # ручка для получения баланса кошелька
async def get_balance(db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    return await wallets_service.get_total_balance(db, current_user)

@router.post('/wallets/', response_model=WalletResponse) # ручка для создания кошелька
async def create_wallet(wallet: CreateWalletRequests, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    return wallets_service.create_wallet(db, current_user, wallet)


@router.get('/wallets', response_model=list[WalletResponse])
def get_all_walletts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return wallets_service.get_all_wallet(db, current_user)