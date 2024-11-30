from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, sessionmaker

from app import crud, schemas
from app.database import engine, Base


# Initialize database tables
Base.metadata.create_all(bind=engine)

router = APIRouter()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        

# Endpoints

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
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@router.delete('/{book_id}', response_model=schemas.Book)
async def delete_book(book_id: str, db: Session = Depends(get_db)):
    book = crud.delete_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book