from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import product, sale  # 🔥 product を必ずインポート

app = FastAPI()

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 ルーター登録
app.include_router(product.router)  # ✅ これがないと `/api/product` が動作しない
app.include_router(sale.router)
