# app/fastapi/routers/segmentation.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import logging

from models.predictor import predictor
from schemas.prediction import PredictionResponse, ErrorResponse
from utils.image_processing import validate_image

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/predict", response_model=PredictionResponse)
async def predict_segmentation(file: UploadFile = File(...)):
    """
    Endpoint pour prédire la segmentation sémantique d'une image
    
    Args:
        file: Image uploadée (JPEG, PNG, etc.)
    
    Returns:
        PredictionResponse: Masque de prédiction et statistiques
    """
    try:
        # Vérifier le type de fichier
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Le fichier doit être une image")
        
        # Lire l'image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Valider l'image
        if not validate_image(image):
            raise HTTPException(status_code=400, detail="Image trop grande (max 4096x4096)")
        
        # Faire la prédiction
        logger.info(f"Prédiction pour l'image: {file.filename}")
        result = predictor.predict(image)
        
        return PredictionResponse(**result)
        
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Vérification de l'état de l'API"""
    return {"status": "healthy", "model_loaded": predictor.model is not None}

@router.get("/model/info")
async def model_info():
    """Informations sur le modèle"""
    return {
        "model_name": "MobileNetV2-UNet",
        "input_size": list(predictor.model.input_shape[1:3]),
        "num_classes": len(predictor.class_mapping['group_names']),
        "class_names": predictor.class_mapping['group_names'],
        "class_colors": predictor.class_mapping['group_colors']
    }