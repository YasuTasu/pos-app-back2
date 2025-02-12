from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, Product  # 修正：Product を正しくインポート
from sqlalchemy import cast, String

# ✅ `router.prefix` を `/api/product` に設定
router = APIRouter(prefix="/api/product", tags=["product"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ すべての商品の一覧を取得するエンドポイント
@router.get("/")
def get_all_products(db: Session = Depends(get_db)):  # ← 関数名を変更
    return db.query(Product).all()


# ✅ JANコードで商品を検索するエンドポイント
@router.get("/{jan}")
def get_product(jan: str, db: Session = Depends(get_db)):
    print(f"🔍 受け取った JAN: '{jan}'（デバッグ用）")  # ここで `JAN` の前後にスペースや特殊文字がないか確認

    # データベースから該当するJANコードの商品を取得
    product = db.query(Product).filter(Product.JAN == jan).first()

    if not product:
        print(f"❌ 商品が見つかりません: '{jan}'")  # `JAN` の値をデバッグ
        raise HTTPException(status_code=404, detail="商品が見つかりません")

    print(f"✅ 商品が見つかりました: {product.name}")  # 見つかった場合のログ

    return {
        "JAN": product.JAN,
        "name": product.name,
        "price": product.price,
    }

