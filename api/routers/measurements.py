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
    
    # -- YENİ EKLENEN KISIM: Duplicate (Çift Kayıt) Kontrolü --
    # Aynı hasta için, aynı zaman damgasına (timestamp) sahip bir veri zaten var mı diye veritabanına soruyoruz.
    existing_record = db.query(models.Measurement).filter(
        models.Measurement.session_id == measurement.patient_id,
        models.Measurement.timestamp == measurement.timestamp
    ).first()

    if existing_record:
        # Eğer veri zaten varsa, sisteme yeni kayıt ekleme ama donanıma "Tamam, bende var" (200 OK) mesajı yolla
        return existing_record
    # ---------------------------------------------------------

    db_measurement = models.Measurement(
        session_id=measurement.patient_id,
        timestamp=measurement.timestamp,
        phase=measurement.phase,
        gsr=measurement.gsr,
        spo2=measurement.spo2,
        pulse=measurement.pulse,
        temp=measurement.temp,
        sbp=measurement.sbp,
        dbp=measurement.dbp
    )
    
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)
    
    return db_measurement

# Cihazdan gelen tüm verileri okuma (GET) - Senin GUI'de kullanacağın kısım
@router.get("/", response_model=list[schemas.MeasurementOut])
def read_measurements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    measurements = db.query(models.Measurement).offset(skip).limit(limit).all()
    return measurements