from fastapi import FastAPI
import uvicorn
from api.routers import measurements # Yazdığımız dosyayı import ettik

app = FastAPI(title="TÜSEB Dental Anksiyete API")

# Router'ı ana uygulamaya dahil et
app.include_router(measurements.router)

@app.get("/")
def read_root():
    return {"mesaj": "API başarıyla çalışıyor! /docs adresine giderek endpointleri test edebilirsiniz."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)