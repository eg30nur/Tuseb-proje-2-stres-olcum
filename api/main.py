from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.routers import measurements
import os
from dotenv import load_dotenv

# .env dosyasındaki gizli değişkenleri sisteme yükler
load_dotenv()

app = FastAPI(title="TÜSEB Dental Anksiyete API")

# CORS Ayarları (Hangi IP'lerin API'ye erişebileceğini belirliyoruz)
origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"  # Şimdilik donanım testleri için herkese açık (*), canlıda sadece spesifik IP'ler olacak
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # GET, POST, PUT hepsine izin ver
    allow_headers=["*"],
)

app.include_router(measurements.router)

@app.get("/")
def read_root():
    # .env dosyasından veri okuma testi
    gizli_anahtar = os.getenv("API_SECRET_KEY", "Bulunamadı")
    return {"mesaj": "API başarıyla çalışıyor!", "durum": "CORS ve Dotenv aktif"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)