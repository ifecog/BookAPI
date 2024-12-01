from sqlalchemy.orm import Session

from app import models
from app.schemas import user_schemas as schemas
from app.utils import hash_password


def create_user(db: Session, user:schemas.UserCreate):
    hashed_password = hash_password(user.password)
    
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_number=user.phone_number,
        password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_phone_number(db: Session, phone_number: str):
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()