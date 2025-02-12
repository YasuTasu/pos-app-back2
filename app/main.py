from fastapi import FastAPI
from app.routes import product, sale
from app.database import get_db  # engine, Base の import は不要になった
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ルーター登録
app.include_router(product.router)
app.include_router(sale.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可（本番環境では制限する）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)