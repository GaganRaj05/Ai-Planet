from fastapi import APIRouter, Depends, HTTPException, Cookie
from jose import JWTError, jwt
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.db.database import SessionLocal
from app.db.models import User
from app.core.security import hash_password, verify_password
from app.utils.token import create_jwt_token
from datetime import datetime, timedelta
from app.core.config import SECRET_KEY, ALGORITHM
from app.utils.db import get_db
router = APIRouter()



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
    except HTTPException:
        raise 
    except Exception as e:
        print(e)
        raise HTTPException(status_code=501,detail="Some error occured please try again later")
        
    
@router.post('/sign-in')
def login_user(user:UserLogin, db:Session=Depends(get_db)):
    try:
        exsisting_user = db.query(User).filter(User.email == user.email).first()
        if not exsisting_user:
            print(exsisting_user)
            raise HTTPException(status_code=400, detail="Account does not exist!")
        pass_match = verify_password(user.password, exsisting_user.password)
        print(pass_match)
        if not pass_match:
            raise HTTPException(status_code=400, detail="Incorrect password entered")
        
        token_data = {"user_id":exsisting_user.id,"email":exsisting_user.email, "name":exsisting_user.name}
        jwt_token = create_jwt_token(token_data)
        response = JSONResponse(content={"message": "Login successful","email":user.email, "name":exsisting_user.name})
        response.set_cookie(
            key="auth_token",
            value= jwt_token,  
            httponly=False,
            max_age=36000, 
            expires=int((datetime.utcnow() + timedelta(hours=10)).timestamp()),  
            samesite="lax",
            secure=False,  
            path="/",     
        )
        return response
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=501, detail="Some error occured please try again later")
    
    
@router.get("/check-auth")
def checkAuth(auth_token:str=Cookie(None)):
    if not auth_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(auth_token, SECRET_KEY,algorithms = [ALGORITHM])
        if email:= payload.get("email"):
            return {"email":email,"name":payload.get("name")}
        raise HTTPException(status_code=401, detail="Token has expired")

    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Some error occured please try again later")
    
    
@router.post("/logout")
async def logout():
    try:
        response = JSONResponse(content={'message':"Logout successfull"})
        response.delete_cookie(
            key="auth_token",
            path="/",
            httponly=False,
            samesite='lax',
        )
        return response
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Some error occured please try again later")