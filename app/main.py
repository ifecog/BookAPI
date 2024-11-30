from fastapi import FastAPI

from app.routes import books, auth

app = FastAPI(
    title='Books CRUD API',
    description='A basic CRUD API for managing books',
    version='1.0.0'
)


app.include_router(books.router, prefix='/books', tags=['Books'])
app.include_router(auth.router, prefix='/users', tags=['users'])


app.get('/')
async def root():
    return {'message': 'Welcome to the Books CRUD API'}