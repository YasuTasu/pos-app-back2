from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# ✅ 環境変数を読み込む
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL が設定されていません！")

print(f"✅ 使用する DATABASE_URL: {DATABASE_URL}")

# ✅ Azure の SSL 証明書パス
ssl_cert_path = "/app/DigiCertGlobalRootCA.crt.pem"  # Azure の推奨パス
if not os.path.exists(ssl_cert_path):
    print("⚠️ SSL 証明書が見つかりません！ 証明書なしで接続します")
    ssl_cert_path = None

connect_args = {"ssl": {"ca": ssl_cert_path}} if ssl_cert_path else {}

# ✅ データベース接続テスト
try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")  # MySQL に問い合わせ
        print("✅ データベース接続確認成功")
except Exception as e:
    print(f"❌ データベース接続エラー: {e}")

# ✅ セッション作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ ベースモデル定義
Base = declarative_base()

# ✅ モデル定義
class Product(Base):
    __tablename__ = "product"
    JAN = Column(String(13), primary_key=True)
    name = Column(String(100))
    price = Column(Integer)

# ✅ セッションの取得関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
