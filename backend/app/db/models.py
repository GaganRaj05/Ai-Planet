from sqlalchemy import Column, Integer, String, TEXT, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
Base = declarative_base()

class User(Base):
    __tablename__ ="users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True)
    password = Column(String, nullable=True)
    pdfs = relationship('PDF', back_populates="user")
    
    
class PDF(Base):
    __tablename__ = "pdf_info"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), ForeignKey('users.email'))  
    pdf_name = Column(String(255))
    pdf_contents = Column(TEXT) 
    
    user = relationship("User", back_populates="pdfs")