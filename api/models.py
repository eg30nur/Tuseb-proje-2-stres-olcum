from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

# Tüm tabloların türetileceği temel sınıf
Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    tc_kimlik = Column(String, unique=True, index=True)
    age = Column(Integer)
    gender = Column(String)

    # Bir hastanın birden fazla ölçüm seansı olabilir (Bire-Çok ilişki)
    sessions = relationship("Session", back_populates="patient")

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id")) # Hangi hastaya ait?
    date = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)

    patient = relationship("Patient", back_populates="sessions")
    measurements = relationship("Measurement", back_populates="session")

class Measurement(Base):
    __tablename__ = "measurements"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id")) # Hangi seansa ait?
    timestamp = Column(Float)  # Donanımdan gelen zaman damgası
    phase = Column(String)     # T0, T1, T2 aşamaları
    gsr = Column(Float)
    spo2 = Column(Float)
    pulse = Column(Float)
    temp = Column(Float)
    sbp = Column(Integer)      # Sistolik Tansiyon
    dbp = Column(Integer)      # Diastolik Tansiyon

    session = relationship("Session", back_populates="measurements")

class MdasResult(Base):
    __tablename__ = "mdas_results"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    total_score = Column(Integer) # 5-25 arası anket skoru