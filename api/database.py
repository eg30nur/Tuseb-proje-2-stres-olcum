from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Veritabanı dosyamızın yolu (alembic'te kurduğumuzla aynı)
SQLALCHEMY_DATABASE_URL = "sqlite:///../db/tuseb_database.db"

# connect_args sadece SQLite'a özel bir ayardır (aynı anda birden fazla isteği yönetmek için)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Her API isteğinde veritabanı bağlantısı açıp, işlem bitince kapatan fonksiyon
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()