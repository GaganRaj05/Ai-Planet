from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.pdf import PDFUploadResponse, QuestionRequest
from app.utils.db import get_db
from app.dependency.dependencies import get_authenticated_email
from app.db.models import PDF
import uuid
import fitz
from app.core.qa_engine import answer_question
from app.db.models import User


router = APIRouter()

@router.post("/upload-pdf", response_model=PDFUploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    email: str = Depends(get_authenticated_email)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files allowed")

    try:
        contents = await file.read()
        

        with fitz.open(stream=contents, filetype="pdf") as doc:
            text = "".join(page.get_text() for page in doc)
            clean_text = text.encode('ascii', errors='ignore').decode('ascii')  
        print(len(clean_text))
        new_pdf = PDF(
            id=str(uuid.uuid4()),  
            email=str(email),     
            pdf_name=str(file.filename),
            pdf_contents=str(clean_text) 
        )
        
        db.add(new_pdf)
        db.commit()
        db.refresh(new_pdf)
        
        return PDFUploadResponse(
            message="PDF uploaded successfully",
            pdf_id=new_pdf.id,
            owner_email=email,
            filename=file.filename,
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Processing error: {str(e)}")
    
@router.get("/pdf")
async def get_pdfs(db:Session=Depends(get_db)):
    try:
        pdfs =  db.query(PDF).all()
        return {"pdf":pdfs}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Some error occured please try again later")
    

@router.post("/ask-question")
async def ask_question(request: QuestionRequest, db: Session = Depends(get_db),email:str = Depends(get_authenticated_email)):
    try:
        db_result = db.query(PDF).filter(PDF.id == request.pdf_id).first()
        pdf_text = db_result.pdf_contents
        answer = await answer_question(pdf_text, f"This is content extracted from a PDF. Now, answer the following question: {request.question}")
        return {"answer": answer}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Some error occured please try again later")