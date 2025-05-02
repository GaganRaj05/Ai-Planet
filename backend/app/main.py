from fastapi import FastAPI
from app.api.routes import auth
from app.db.database import init_db
import uvicorn

app = FastAPI()
init_db()

app.include_router(auth.router, prefix="/auth")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
