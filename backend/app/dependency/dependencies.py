from fastapi import Cookie, HTTPException
from jose import JWTError, jwt
from app.core.config import SECRET_KEY, ALGORITHM

async def get_authenticated_email(auth_token: str = Cookie(None)) -> str:
    if not auth_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=[ALGORITHM])
        if email := payload.get("email"):
            return email
        raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError as e:
        print(f"JWT Error: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")
    
    