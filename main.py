from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1.wallets import router as wallet_router
from app.api.v1.operations import router as operations_router
from app.api.v1.users import router as users_router
from app.database import Base, engine

# инициализация FastAPI приложения
app = FastAPI()

app.include_router(wallet_router, prefix='/api/v1', tags=['wallets'])
app.include_router(operations_router, prefix='/api/v1', tags=['operations'])
app.include_router(users_router, prefix='/api/v1', tags=['users'])


app.mount('/static', StaticFiles(directory='app/static'), name='static')

# создаем все таблицы в базе данных при старте приложения
Base.metadata.create_all(bind=engine)