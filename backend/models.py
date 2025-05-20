from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

# Bu dosya içinde veritabanı tabloları oluşturuyoruz

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) 
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    files = relationship("File", back_populates="owner") # Bir kullanıcının birden fazla dosyası olabilir. İlişki back_populates ile kuruluyor.

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    file_path = Column(String)
    file_type = Column(String)
    upload_date = Column(DateTime, default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id")) # Bir kullanıcının birden fazla dosyası olabilir. İlişki foreign key ile kuruluyor.

    owner = relationship("User", back_populates="files") # Bir dosyanın bir kullanıcısı olabilir. İlişki back_populates ile kuruluyor.