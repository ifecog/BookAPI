from sqlalchemy.orm import sessionmaker
from app.database import engine


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
