from fastapi import FastAPI

from app.api.v1.wallets import router as wallet_router
from app.api.v1.operations import router as operations_router
from app.database import Base, engine

# инициализация FastAPI приложения
app = FastAPI()

app.include_router(wallet_router, prefix='/api/v1', tags=['wallets'])
app.include_router(operations_router, prefix='/api/v1', tags=['operations'])

Base.metadata.create_all(bind=engine)