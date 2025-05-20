from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from datetime import timedelta
from database import get_db, engine
import models
import auth
from pydantic import BaseModel
import shutil
from pathlib import Path
from sqlalchemy import or_

# Bu dosya içinde FastAPI uygulaması çalıştırılıyor. Ana işlemler burada yapılıyor.

# Veritabanı tablolarını oluşturduk. Böylece sql_app.db dosyasını oluşturuyoruz.   
models.Base.metadata.create_all(bind=engine)    

app = FastAPI() 

# CORS ayarları. Bu ayarlar sayesinde React uygulamasının çalışacağı adreslere erişim sağlanıyor. Hata engellenmiş olur.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React uygulamasının çalışacağı adres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dosya yükleme klasörü
UPLOAD_FOLDER = "uploaded_files" 
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Pydantic modelleri  
class UserCreate(BaseModel): # Frontend tarafından gönderilen verilerin formatını belirliyoruz.
    username: str
    email: str
    password: str

class Token(BaseModel): # Giriş yapıldıktan sonra dönen token'ın formatını belirliyoruz.
    access_token: str
    token_type: str

class FileResponse(BaseModel): # Bir dosya yüklenip başarıyla kaydedildikten sonra, dosya bilgilerini frontend'e dönerken kullanılır.
    id: int
    filename: str
    file_type: str
    upload_date: str

# Kullanıcı kaydı
@app.post("/api/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Zaten bir email ve kullanıcı adı ile kayıt olunmuş mu kontrol ediliyor.
    db_user = db.query(models.User).filter(
        or_(
            models.User.username == user.username,
            models.User.email == user.email
        )
    ).first()
    if db_user: # Eğer kullanıcı varsa hata döndürülür.
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )   
    
    # Yeni kullanıcı oluştur
    hashed_password = auth.get_password_hash(user.password) 
    db_user = models.User(  
        username=user.username, # Kullanıcı adı veritabanına kaydediliyor. Burada sağ taraftaki "user" "UserCreate"ten oluşan bir nesnedir. Bu da frontend tarafından gönderilen "user" olduğu anlamına gelir.
        email=user.email, # Sağdaki user frontend tarafından gönderilen user'dır.
        hashed_password=hashed_password
    )
    db.add(db_user) # Veritabanına eklenecekler listesine ekleniyor.
    db.commit() # Veritabanına kalıcı olarak kaydeder.
    db.refresh(db_user) 
     

    # Token oluştur
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"} # Token döndürülüyor.

# Kullanıcı girişi
@app.post("/api/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): 
    # form_data: OAuth2PasswordRequestForm = Depends() kısmı hazır bir kalıp gibi kullanılır. Buradan form_data.username ve form_data.password alınır.
    user = db.query(models.User).filter(models.User.username == form_data.username).first() 
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token( # Kullanıcı başarıyla giriş yapıldıktan sonra token oluşturuluyor.
        data={"sub": user.username},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"} # Token döndürülüyor.

# Dosya yükleme
@app.post("/api/upload", response_model=FileResponse)
async def upload_file( 
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Dosya uzantısını kontrol et
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ['.pdf', '.png', '.jpg']:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, PNG and JPG files are allowed"
        )
    
    # Dosyayı kaydet
    file_path = os.path.join(UPLOAD_FOLDER, file.filename) 
    with open(file_path, "wb") as buffer: 
        shutil.copyfileobj(file.file, buffer) 
    
    # Veritabanına kaydet
    db_file = models.File( 
        filename=file.filename,
        file_path=file_path,
        file_type=file_ext[1:],  # nokta olmadan uzantıyı kaydet
        owner_id=current_user.id
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    return {
        "id": db_file.id,
        "filename": db_file.filename,
        "file_type": db_file.file_type,
        "upload_date": db_file.upload_date.isoformat()
    }

# Dosyaları listele
@app.get("/api/files", response_model=List[FileResponse])
def list_files(
    current_user: models.User = Depends(auth.get_current_user), # Token doğrulama işlemi.
    db: Session = Depends(get_db)  # Veritabanı bağlantısı.
):
    files = db.query(models.File).filter(models.File.owner_id == current_user.id).all() # Veritabanından dosya sorgusu yapılıyor.
    return [ 
        {
            "id": file.id,
            "filename": file.filename,
            "file_type": file.file_type,
            "upload_date": file.upload_date.isoformat()
        }
        for file in files # Dosya bilgileri döndürülüyor.
    ]

# Dosya sil
@app.delete("/api/files/{file_id}")
def delete_file(
    file_id: int,
    current_user: models.User = Depends(auth.get_current_user), # Token doğrulama işlemi.
    db: Session = Depends(get_db)  # Veritabanı bağlantısı.
):
    file = db.query(models.File).filter(
        models.File.id == file_id,
        models.File.owner_id == current_user.id
    ).first()
    
    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
    
    # Dosyayı fiziksel olarak sil
    try:
        os.remove(file.file_path)
    except OSError:
        pass  # Dosya zaten silinmiş olabilir
    
    # Veritabanından sil
    db.delete(file)
    db.commit()
    
    return {"message": "File deleted successfully"}

@app.get("/") 
async def root(): 
    return {"message": "File Upload API"}  