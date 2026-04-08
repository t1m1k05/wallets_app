from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import OperationRequest
from app.repository import wallets as wallets_repository


def add_income(db: Session, current_user: User, operation: OperationRequest):
    # Проверяем существование кошелька
    if not wallets_repository.is_wallet_exist(db, current_user.id, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )

    # Обновляем баланс
    wallet = wallets_repository.add_income(db, current_user.id, operation.wallet_name, operation.amount)
    db.commit()

    return {
        'message': "Income added",
        'wallet': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': wallet.balance,
    }


def add_expense(db: Session, current_user: User, operation: OperationRequest):
    # Проверяем существование кошелька
    if not wallets_repository.is_wallet_exist(db, current_user.id, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )

    # Проверяем достаточно ли средств
    wallet = wallets_repository.get_wallet_balance_by_name(db, current_user.id, operation.wallet_name)
    if wallet.balance < operation.amount:
        raise HTTPException(
            status_code=400,  # 400 Bad Request, а не 404
            detail=f'Insufficient funds. Available: {wallet.balance}'
        )

    # Обновляем баланс
    wallet = wallets_repository.add_expense(db, current_user.id, operation.wallet_name, operation.amount)
    db.commit()


    return {
        'message': "Expense added",
        'wallet': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': wallet.balance,
    }


