from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base
from app.core.config import DATABASE_URL
#create a db engine to connect to a sqllite db
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread":False})
#session to interact with the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

#initalising the imported models in the db
def init_db():
    Base.metadata.create_all(bind=engine)