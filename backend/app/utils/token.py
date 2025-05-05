import jwt
from datetime import datetime, timedelta
from typing import Union, Any
from app.core.config import SECRET_KEY, ALGORITHM

#helper function to create jwt token
def create_jwt_token(data: dict, expires_delta: timedelta = timedelta(hours=1)) -> str:
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(
            to_encode, 
            SECRET_KEY, 
            algorithm=ALGORITHM
        )
        
            
        return encoded_jwt
        
    except Exception as e:
        raise ValueError(f"Token creation error: {str(e)}")