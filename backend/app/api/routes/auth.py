from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.db.database import SessionLocal
from app.db.models import User
from app.core.security import hash_password, verify_password
from app.utils.token import create_jwt_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


@router.post('/sign-up')
async def register_user(user:UserCreate, db:Session=Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Account exists")
        
        hashed_pwd = hash_password(user.password)
        new_user = User(
            name = user.name,
            email= user.email,
            password = hashed_pwd
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message":"User created successfully","user_id":new_user.id}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=501,detail="Some error occured please try again later")
        
    
@router.post('/sign-in')
def login_user(user:UserLogin, db:Session=Depends(get_db)):
    try:
        exsisting_user = db.query(User).filter(User.email == user.email).first()
        if not exsisting_user:
            raise HTTPException(status_code=400, detail="Account does not exist!")
        pass_match = verify_password(user.password, exsisting_user.password)
        if not pass_match:
            raise HTTPException(status_code=400, detail="Incorrect password entered")
        
        token_data = {"user_id":exsisting_user.id,"email":exsisting_user.email}
        jwt_token = create_jwt_token(token_data)
        
        response = JSONResponse(content={"message": "Login successful"})
        response.set_cookie(
            key="auth_token",
            value=jwt_token,
            httponly=True,
            max_age=3600,
            expires=3600,
            samesite="lax",
            secure=False
        )
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=501, detail="Some error occured please try again later")