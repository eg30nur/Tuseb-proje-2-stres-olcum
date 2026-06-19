from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.database import get_db
from api import models, schemas

router = APIRouter(
    prefix="/measurements",
    tags=["Measurements"]
)

# ESP32'den gelen veriyi veritabanına kaydetme (POST)
@router.post("/", response_model=schemas.MeasurementOut, status_code=status.HTTP_201_CREATED)
def create_measurement(measurement: schemas.MeasurementIn, db: Session = Depends(get_db)):
    
    # 1. Pydantic ile gelen veriyi (schemas) veritabanı modeline (models) çeviriyoruz
    db_measurement = models.Measurement(
        session_id=measurement.patient_id, # Şimdilik session_id yerine patient_id kullanıyoruz (ileride düzelteceğiz)
        timestamp=measurement.timestamp,
        phase=measurement.phase,
        gsr=measurement.gsr,
        spo2=measurement.spo2,
        pulse=measurement.pulse,
        temp=measurement.temp,
        sbp=measurement.sbp,
        dbp=measurement.dbp
    )
    
    # 2. Veritabanına ekle ve kaydet (C++'taki pointer ile bellek adresine yazmak gibi düşünebilirsin)
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement) # Veritabanından oluşan otomatik ID'yi çekmek için
    
    return db_measurement

# Cihazdan gelen tüm verileri okuma (GET) - Senin GUI'de kullanacağın kısım
@router.get("/", response_model=list[schemas.MeasurementOut])
def read_measurements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    measurements = db.query(models.Measurement).offset(skip).limit(limit).all()
    return measurements