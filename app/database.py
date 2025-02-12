from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# .env ファイルの読み込み
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL が設定されていません。")

# SSL 証明書のパスを設定
ssl_cert_path = "C:/Users/81804/OneDrive/デスクトップ/GLOBIS/Tech0/Step4/pos-app/backend/app/DigiCertGlobalRootCA.crt.pem"
connect_args = {"ssl": {"ca": ssl_cert_path}}

# MySQL エンジン作成（接続安定性向上のため pool_pre_ping=True を追加）
engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)

# セッション作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースモデル定義
Base = declarative_base()

# モデル定義
class Product(Base):
    __tablename__ = "product"
    JAN = Column(String(13), primary_key=True)
    name = Column(String(100))
    price = Column(Integer)

# セッションの取得関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
