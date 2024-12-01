from sqlalchemy.orm import Session

from app import models
from app.schemas import book_schemas as schemas


def get_books(db: Session):
    return db.query(models.Book).all()


def get_book(db: Session, book_id: str):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate, user_id: UUID):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    return db_book


def delete_book(db: Session, book_id: str):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    
    return db_book

