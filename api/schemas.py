from pydantic import BaseModel
from typing import Optional

# Donanımdan (POST) API'ye gelecek sensör verisinin şablonu
class MeasurementIn(BaseModel):
    patient_id: int
    phase: str
    timestamp: float
    gsr: float
    spo2: float
    pulse: float
    temp: float
    sbp: int
    dbp: int

# API'den arayüze (GET) gönderilecek sensör verisinin şablonu
class MeasurementOut(MeasurementIn):
    id: int
    session_id: int

    class Config:
        from_attributes = True  # SQLAlchemy modeli ile Pydantic'in uyumlu çalışmasını sağlar

# Yeni bir seans başlatırken kullanılacak şablon
class SessionCreate(BaseModel):
    patient_id: int
    notes: Optional[str] = None