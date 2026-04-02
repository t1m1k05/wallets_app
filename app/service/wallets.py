from fastapi import HTTPException, Query
from typing import Annotated

from app.database import SessionLocal
from app.schemas import CreateWalletRequests
from app.repository import wallets as wallets_repository


def get_balance(wallet_name: Annotated[str | None, Query()] = None):
    db = SessionLocal()
    try:
        # Если имя кошелька не указано - считаем общий баланс
        if wallet_name is None:
            wallets = wallets_repository.get_all_wallets(db)
            return {'total_balance': sum([w.amount for w in wallets])}
        # Проверяем существует ли запрашиваемый кошелек
        if not wallets_repository.is_wallet_exist(db, wallet_name=wallet_name):
            raise HTTPException(
                status_code=404,
                detail=f'Wallet {wallet_name} not found'
            )

        # Возвращаем баланс конкретного кошелька
        wallet = wallets_repository.get_wallet_balance_by_name(db, wallet_name)
        return {'wallet': wallet.name, 'balance': wallet.balance}
    finally:
        db.close()


def create_wallet(wallet: CreateWalletRequests):
    db = SessionLocal()
    try:
        if wallets_repository.is_wallet_exist(db, wallet_name=wallet.name):
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{wallet.name}' already exist"
            )
        wallet = wallets_repository.create_wallet(db, wallet.name, wallet.initial_balance)
        db.commit()
        return {
            'message': f'Wallet {wallet.name} created',
            'wallet': wallet.name,
            'balance': wallet.balance
        }
    finally:
        db.close()

