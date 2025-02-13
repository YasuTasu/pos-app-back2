from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# ✅ 環境変数を読み込む
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL が設定されていません！")

# ✅ デバッグ用ログ（Azure のログで確認する）
print(f"✅ 使用する DATABASE_URL: {DATABASE_URL}")

# ✅ SSL 証明書パスの設定（環境変数から取得可能にする）
ssl_cert_path = os.getenv("SSL_CERT_PATH", "/home/site/wwwroot/DigiCertGlobalRootCA.crt.pem")

# 🔥 Azure でもローカルでも `SSL_CERT_PATH` がない場合は無視
if ssl_cert_path and not os.path.exists(ssl_cert_path):
    print(f"⚠️ 指定された SSL 証明書が見つかりません: {ssl_cert_path}")
    ssl_cert_path = None

# ✅ MySQL エンジン作成（pool_pre_ping=True で接続安定化）
connect_args = {"ssl": {"ca": ssl_cert_path}} if ssl_cert_path else {}

try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
    connection = engine.connect()  # 🔥 DB 接続テスト
    print("✅ データベース接続成功")
    connection.close()  # 明示的にクローズ
except Exception as e:
    print(f"❌ データベース接続失敗: {e}")

# ✅ セッション作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ ベースモデル定義
Base = declarative_base()

# ✅ モデル定義
class Product(Base):
    __tablename__ = "product"  # 🔥 MySQL では小文字に統一
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
