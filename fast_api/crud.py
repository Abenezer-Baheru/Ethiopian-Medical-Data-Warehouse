from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

# Function to get detection data from the database
async def get_detection_data(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.DetectionData).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to create new detection data in the database
async def create_detection_data(db: Session, detection_data: schemas.DetectionDataCreate):
    try:
        db_detection_data = models.DetectionData(**detection_data.dict())
        db.add(db_detection_data)
        db.commit()
        db.refresh(db_detection_data)
        return db_detection_data
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))