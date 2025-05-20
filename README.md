# Dosya Yükleme Sistemi

Bu proje, kullanıcıların PDF, PNG ve JPG dosyalarını yükleyip yönetebilecekleri basit bir web uygulamasıdır.

## Kullanılan Teknolojiler

### Backend
- FastAPI
- SQLite
- SQLAlchemy
- JWT Authentication
- Python 3.8+

### Frontend
- React
- React Router
- Axios
- CSS

## Kurulum

### Backend Kurulumu

1. Backend klasörüne gidin:
```bash
cd backend
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac için
# veya
.\venv\Scripts\activate  # Windows için
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. Uygulamayı çalıştırın:
```bash
uvicorn main:app --reload
```

### Frontend Kurulumu

1. Frontend klasörüne gidin:
```bash
cd frontend
```

2. Gerekli paketleri yükleyin:
```bash
npm install
```

3. Uygulamayı çalıştırın:
```bash
npm start
```

## API Uç Noktaları

- POST /api/register - Kullanıcı kaydı
- POST /api/login - Kullanıcı girişi
- POST /api/upload - Dosya yükleme
- GET /api/files - Kullanıcının dosyalarını listeleme
- DELETE /api/files/{file_id} - Dosya silme

## Özellikler

- JWT tabanlı kimlik doğrulama
- Dosya yükleme (PDF, PNG, JPG)
- Dosya listeleme
- Dosya silme
- Kullanıcıya özel dosya yönetimi

## Test Notu

JWT ile korumalı endpoint'ler (dosya yükleme, listeleme, silme) Swagger UI'da test edilemez. Bu işlemler için terminalde curl komutları kullanılmalıdır. 