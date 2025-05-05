from passlib.context import CryptContext
#security helper functions, used typically for password hashing and hashpassword verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_pass: str, hash_pass: str) -> bool:
    return pwd_context.verify(plain_pass, hash_pass)