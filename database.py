from sqlalchemy import create_engine, Column, String, DateTime, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://medicinebot:secure_password_here@localhost:5432/medicine_quality_db")

# Create engine
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Database Models
class Medicine(Base):
    """Medicine information model"""
    __tablename__ = "medicines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    type = Column(String(100))
    manufacturer = Column(String(255))
    active_ingredient = Column(String(255))
    dosage = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MedicineBatch(Base):
    """Medicine batch tracking model"""
    __tablename__ = "medicine_batches"
    
    id = Column(Integer, primary_key=True, index=True)
    batch_number = Column(String(100), unique=True, index=True)
    medicine_id = Column(Integer, index=True)
    manufacturing_date = Column(DateTime)
    expiry_date = Column(DateTime)
    quantity = Column(Integer)
    quality_score = Column(Float)
    status = Column(String(50))  # verified, counterfeit, suspicious
    qr_code = Column(String(1000))
    created_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime)

class ChatHistory(Base):
    """Chat conversation history model"""
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)
    message = Column(String(1000))
    response = Column(String(2000))
    medicine_name = Column(String(255))
    batch_number = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

class SideEffect(Base):
    """Medicine side effects model"""
    __tablename__ = "side_effects"
    
    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, index=True)
    effect_name = Column(String(255))
    severity = Column(String(50))  # mild, moderate, severe
    frequency = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class DrugInteraction(Base):
    """Drug interaction database model"""
    __tablename__ = "drug_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    medicine_id_1 = Column(Integer, index=True)
    medicine_id_2 = Column(Integer, index=True)
    interaction_type = Column(String(255))  # major, moderate, minor
    description = Column(String(1000))
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency function for FastAPI
def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
