from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.crud import books_crud as crud
from app.dependencies import get_db
from app.schemas import book_schemas as schemas
from app.schemas import user_schemas as user_schemas
from app.utils import get_current_user


router = APIRouter()

@router.get('/', response_model=list[schemas.Book])
async def read_books(db: Session = Depends(get_db)):
    return crud.get_books(db)


@router.get('/{book_id}', response_model=schemas.Book)
async def read_book(book_id: str, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f'Book with the id of {book_id} not found')
    
    return book


@router.post('/', response_model=schemas.Book)
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), current_user: user_schemas.UserOut = Depends(get_current_user)):
    return crud.create_book(db, book)


@router.delete('/{book_id}', response_model=schemas.Book)
async def delete_book(book_id: str, db: Session = Depends(get_db)):
    book = crud.delete_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book