from fastapi import FastAPI
from app.api.routes import auth, pdf
from app.db.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
app = FastAPI()

#middleware to set hosts 
app.add_middleware(TrustedHostMiddleware, allowed_hosts=['*'])

#cors for cross origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:5173','https://ai-pdf-scanner-by-gagan.netlify.app'],
    allow_credentials = True,
    allow_methods=['*'],
    allow_headers = ['*']
)

#used to compress the http responses 
app.add_middleware(GZipMiddleware, minimum_size=1000)
init_db()#initailise the models in the db

#initialising the router
app.include_router(auth.router, prefix="/auth")
app.include_router(pdf.router, prefix='/uploads')
#running the app on uvicorn asgi server 

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
