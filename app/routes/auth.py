from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.crud import users_crud as crud
from app.database import engine, Base
from app.dependencies import get_db
from app.schemas import user_schemas as schemas
from app.utils import verify_password, create_access_token


Base.metadata.create_all(bind=engine)

router = APIRouter()
        
@router.post('/signup', response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail='Email already in use!')
    if crud.get_user_by_phone_number(db, user.phone_number):
        raise HTTPException(status_code=400, detail='Phone number already in use!')
    
    return crud.create_user(db, user)


@router.post('/signin', response_model=schemas.Token)
def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    access_token = create_access_token(data={'sub': user.email})
    
    return {'access_token': access_token, 'token_type': 'bearer'}