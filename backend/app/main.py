from fastapi import FastAPI
from app.api.routes import auth, pdf
from app.db.database import init_db
import uvicorn
app = FastAPI()
init_db()

app.include_router(auth.router, prefix="/auth")
app.include_router(pdf.router, prefix='/uploads')
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
