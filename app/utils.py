from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from decouple import config

from app.crud.users_crud import get_user_by_email
from app.dependencies import get_db
from app.schemas.user_schemas import TokenData


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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/signin')

def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail='Could not validate credentials!'
        headers={'WWW-Authenticate': 'Bearer'}
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    
    return user
    