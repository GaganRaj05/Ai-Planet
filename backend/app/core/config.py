from dotenv import load_dotenv
import os

load_dotenv()
#general config file to make the env variables accessible to every other module of the app
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
GROQAI_API_KEY = os.getenv("GROQAI_API_KEY")
