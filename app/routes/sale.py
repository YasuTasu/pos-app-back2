from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product

router = APIRouter(prefix="/sales", tags=["sales"])

# 売上登録
@router.post("/")
def register_sale(product_id: int, quantity: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="在庫不足")

    product.stock -= quantity
    db.commit()
    
    return {"message": "売上が登録されました", "remaining_stock": product.stock}
