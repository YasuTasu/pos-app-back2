from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, Product  # `get_db` を database.py からインポート
from sqlalchemy import cast, String

# ✅ `router.prefix` を `/api/product` に設定
router = APIRouter(prefix="/api/product", tags=["product"])

# ✅ すべての商品の一覧を取得するエンドポイント
@router.get("/")
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    if not products:
        raise HTTPException(status_code=404, detail="商品が登録されていません")
    return products

# ✅ JANコードで商品を検索するエンドポイント
@router.get("/{jan}")
def get_product(jan: str, db: Session = Depends(get_db)):
    print(f"🔍 受け取った JAN: '{jan}'（デバッグ用）")  

    # 🔥 `cast` を使用して JAN を文字列として比較
    product = db.query(Product).filter(cast(Product.JAN, String) == jan).first()

    if not product:
        print(f"❌ 商品が見つかりません: '{jan}'")  
        raise HTTPException(status_code=404, detail="商品が見つかりません")

    print(f"✅ 商品が見つかりました: {product.name}")  

    return {
        "JAN": product.JAN,
        "name": product.name,
        "price": product.price,
    }

# ✅ デバッグ用エンドポイント: DB 接続テスト & 商品データ確認
@router.get("/debug")
def debug(db: Session = Depends(get_db)):
    try:
        result = db.execute("SELECT * FROM product LIMIT 1").fetchall()
        return {"status": "✅ DB 接続成功", "data": result}
    except Exception as e:
        return {"status": "❌ DB 接続失敗", "error": str(e)}
