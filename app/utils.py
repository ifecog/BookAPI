from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from decouple import config


# Password hashing
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# JWT configuration
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRES_MINUTES = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({'exp': expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 