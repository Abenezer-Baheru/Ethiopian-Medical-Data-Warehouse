from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection URL
DATABASE_URL = 'postgresql://postgres:abeni@localhost:5432/telegram_data'

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the declarative model
Base = declarative_base()

# Dependency to get the database session
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()