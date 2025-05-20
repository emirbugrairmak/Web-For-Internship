from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Bu dosya içinde veritabanı bağlantısı oluşturuluyor.

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"   # Veritabanı URL'si

engine = create_engine(   
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# Veritabanı ile bağlantı kurmak için oturum (session) oluşturuluyor.

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 