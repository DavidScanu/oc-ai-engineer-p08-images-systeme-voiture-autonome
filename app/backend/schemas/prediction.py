# app/backend/schemas/prediction.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ClassStatistic(BaseModel):
    class_id: int
    class_name: str
    pixel_count: int
    percentage: float

class ImageSet(BaseModel):
    original: str  # base64
    prediction_mask: str  # base64
    overlay: str  # base64
    side_by_side: str  # base64

class PredictionResponse(BaseModel):
    class_statistics: List[ClassStatistic]
    image_size: List[int]
    segmented_image_size: List[int]
    num_classes: int
    dominant_class: str
    dominant_class_percentage: float
    timestamp: str
    filename: str
    images: ImageSet
    artifacts_path: str

class ErrorResponse(BaseModel):
    error: str
    detail: str