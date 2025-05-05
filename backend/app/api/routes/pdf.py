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
#Route for uploading pdf
@router.post("/upload-pdf", response_model=PDFUploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),#File uploads
    db: Session = Depends(get_db), #db session for interacting with sqllite
    email: str = Depends(get_authenticated_email)# dependency injection to check if the user's authenticated before uploading the pdf
):
    #check if pdf files are uploaded otherwise raise an error
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files allowed")

    try:
        #read the contents of file
        contents = await file.read()
        
        #fitz to open the binary data stored in the contents as a stream
        with fitz.open(stream=contents, filetype="pdf") as doc:
            #text stores the raw data from every page 
            text = "".join(page.get_text() for page in doc)#loops through each page in the doc, page.get_text extracts all text from the current page as a single string
            clean_text = text.encode('ascii', errors='ignore').decode('ascii') #clean the text by removing no ascii characters and converts the cleaned bytes back to string 
        print(len(clean_text))
        #data to insert pdf info into the db
        new_pdf = PDF(
            id=str(uuid.uuid4()), #generate a random unique id  
            email=str(email),     
            pdf_name=str(file.filename),
            pdf_contents=str(clean_text) 
        )
        #insert new pdf in the db
        db.add(new_pdf)
        db.commit()
        db.refresh(new_pdf)
        
        #return pdf_id, pdf_name to frontend
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
    
#Route defined for testing purposes to check if the pdf uploads are properly done
@router.get("/pdf")
async def get_pdfs(db:Session=Depends(get_db)):
    try:
        #retrive all the pdfs
        pdfs =  db.query(PDF).all()
        return {"pdf":pdfs}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Some error occured please try again later")
    
#route for users to ask questions based on the uploaded pdf
@router.post("/ask-question")
async def ask_question(request: QuestionRequest, db: Session = Depends(get_db),email:str = Depends(get_authenticated_email)):
    try:
        #retrieve the pdf document that was uploaded
        db_result = db.query(PDF).filter(PDF.id == request.pdf_id).first()
        #store the contents for quering with the model
        pdf_text = db_result.pdf_contents
        #parse the question to the model with the question
        answer = await answer_question(pdf_text, f"This is content extracted from a PDF. Now, answer the following question: {request.question}")
        #return the answer from the model
        return {"answer": answer}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Some error occured please try again later")