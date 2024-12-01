from pydantic import BaseModel
from uuid import UUID

class BookBase(BaseModel):
    title: str
    author: str
    year: int
    description: str | None = None
    

class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: UUID
    
    class Config:
        orm_mode = True
        
