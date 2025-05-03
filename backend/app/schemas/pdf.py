from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PDFUploadBase(BaseModel):
    pass  

class PDFUploadResponse(BaseModel):
    message: str
    pdf_id: str = Field(..., example="550e8400-e29b-41d4-a716-446655440000")
    owner_email: str = Field(..., example="user@example.com")
    filename: str = Field(..., example="document.pdf")
    
    class Config:
        orm_mode = True  