# app/fastapi/schemas/prediction.py
from pydantic import BaseModel
from typing import List, Dict, Any

class ClassStatistic(BaseModel):
    class_id: int
    class_name: str
    pixel_count: int
    percentage: float

class PredictionResponse(BaseModel):
    prediction_mask: List[List[int]]
    colored_mask: List[List[List[int]]]
    class_statistics: List[ClassStatistic]
    image_size: List[int]
    num_classes: int

class ErrorResponse(BaseModel):
    error: str
    detail: str