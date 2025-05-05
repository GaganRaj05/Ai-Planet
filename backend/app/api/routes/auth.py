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


#Sign up route for creating an account
@router.post('/sign-up')#get_db method which provides  db session to the route which is then added as dependency injection
async def register_user(user:UserCreate, db:Session=Depends(get_db)):
    try:
        #check if the user account already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            #if it does then raise an error
            raise HTTPException(status_code=400, detail="Account exists")
        
        #hash the password
        hashed_pwd = hash_password(user.password)
        new_user = User(
            name = user.name,
            email= user.email,
            password = hashed_pwd
        )
        #storing user info in the db
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        #returning user credentials to frontend after successfull account creation
        return {"message":"User created successfully","user_id":new_user.id}
    except HTTPException:
        raise 
    except Exception as e:
        print(e)
        #incase any internal error occurs 
        raise HTTPException(status_code=500,detail="Some error occured please try again later")
        

#Route for Login
@router.post('/sign-in')#get_db method which provides  db session to the route which is then added as dependency injection
def login_user(user:UserLogin, db:Session=Depends(get_db)):
    try:
        #check if user account exists
        exsisting_user = db.query(User).filter(User.email == user.email).first()
        #if not raise an error
        if not exsisting_user:
            print(exsisting_user)
            raise HTTPException(status_code=400, detail="Account does not exist!")
        #check user password is same as the hashed password in the db 
        pass_match = verify_password(user.password, exsisting_user.password)
        print(pass_match)
        #if not raise an error
        if not pass_match:
            raise HTTPException(status_code=400, detail="Incorrect password entered")
        #store the token data
        token_data = {"user_id":exsisting_user.id,"email":exsisting_user.email, "name":exsisting_user.name}
        #create a jwt 
        jwt_token = create_jwt_token(token_data)
        #response to be sent after successfull login
        response = JSONResponse(content={"message": "Login successful","email":user.email, "name":exsisting_user.name})
        #set cookie after login to establish cookie based authentication
        response.set_cookie(
            key="auth_token",#key to access the cookie value
            value= jwt_token, #actual cookie value
            httponly=True, 
            max_age=36000, 
            expires=int((datetime.utcnow() + timedelta(hours=10)).timestamp()),  
            samesite="Lax",
            secure=True,  
            path="/",     
        )
        return response
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        #incase any internal error occurs 

        raise HTTPException(status_code=501, detail="Some error occured please try again later")
    
#Route to manage authcontext in frontend
@router.get("/check-auth")#takes cookie stored in the browser as arguement
def checkAuth(auth_token:str=Cookie(None)):
    #check if the auth_token sent during login exists if it does not then raise an error
    if not auth_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        #decode the jwt token and verify it's legitamacy
        payload = jwt.decode(auth_token, SECRET_KEY,algorithms = [ALGORITHM])
        if email:= payload.get("email"):
            #send the user context to frontend
            return {"email":email,"name":payload.get("name")}
        #if token has expired raise an error
        raise HTTPException(status_code=401, detail="Token has expired")

    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Some error occured please try again later")
    
    
#Route for logout
@router.post("/logout")
async def logout():
    try:
        #response to sent after logging out
        response = JSONResponse(content={'message':"Logout successfull"})
        #clear the cookie stored in the browser 
        response.delete_cookie(
            key="auth_token",
            path="/",
            httponly=False,
            samesite='Lax',
        )
        return response
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Some error occured please try again later")