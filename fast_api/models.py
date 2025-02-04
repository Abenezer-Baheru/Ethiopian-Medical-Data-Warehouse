from sqlalchemy import Column, Integer, Float, String, JSON
from .database import Base

# Define the DetectionData model
class DetectionData(Base):
    __tablename__ = 'detection_data'
    
    id = Column(Integer, primary_key=True, index=True)  # Primary key
    bounding_box = Column(JSON)  # JSON column for bounding box coordinates
    confidence = Column(Float)  # Confidence score
    class_id = Column(Integer)  # Class ID
    class_name = Column(String)  # Class name
    image_path = Column(String)  # Path to the image