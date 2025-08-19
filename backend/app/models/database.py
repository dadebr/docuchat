from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./docuchat.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class DocumentCollection(Base):
    __tablename__ = "document_collections"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    document_count = Column(Integer, default=0)

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(Integer, index=True)
    filename = Column(String(255))
    original_name = Column(String(255))
    file_path = Column(String(500))
    file_size = Column(Integer)
    content_type = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_indexed = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)
