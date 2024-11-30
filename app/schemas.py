from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

# Book Model
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
        
        
# User Model
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$') 
    
    
class UserCreate(UserBase):
    password: str
    
    
class UserOut(UserBase):
    id: UUID
    is_active: bool
    
    class Config:
        orm_mode = True
        

# Token
class Token(BaseModel):
    access_token: str
    token_type: str