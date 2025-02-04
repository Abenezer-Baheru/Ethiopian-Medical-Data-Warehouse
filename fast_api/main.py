from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import SessionLocal, engine

# Create all the tables in the database
models.Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI()

# Dependency to get the database session
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to create new detection data
@app.post("/detection_data/", response_model=schemas.DetectionData)
async def create_detection_data(detection_data: schemas.DetectionDataCreate, db: Session = Depends(get_db)):
    try:
        return await crud.create_detection_data(db=db, detection_data=detection_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to read detection data
@app.get("/detection_data/", response_model=List[schemas.DetectionData])
async def read_detection_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        detection_data = await crud.get_detection_data(db, skip=skip, limit=limit)
        return detection_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))