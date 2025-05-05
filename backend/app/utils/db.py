from app.db.database import SessionLocal

#helper function get a db sesssion for db interaction

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
