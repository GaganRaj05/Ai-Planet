from pydantic import BaseModel
#schemas to validate incoming form data's

class UserCreate(BaseModel):
    name:str
    email:str
    password:str
    
class UserLogin(BaseModel):
    email:str
    password:str