from pydantic import BaseModel, EmailStr
#schemas to validate incoming form data's

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str
    
class UserLogin(BaseModel):
    email:EmailStr
    password:str