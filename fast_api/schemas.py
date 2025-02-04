from pydantic import BaseModel
from typing import List

# Base schema for detection data
class DetectionDataBase(BaseModel):
    bounding_box: List[int]
    confidence: float
    class_id: int
    class_name: str
    image_path: str

# Schema for creating detection data
class DetectionDataCreate(DetectionDataBase):
    pass

# Schema for reading detection data with ID
class DetectionData(DetectionDataBase):
    id: int

    # Config class to enable ORM mode
    class Config:
        orm_mode = True