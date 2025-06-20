# app/backend/routers/segmentation.py
import json
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
        PredictionResponse: Masques, visualisations et statistiques
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
        
        # Faire la prédiction avec génération des artefacts
        logger.info(f"Prédiction pour l'image: {file.filename}")
        result = predictor.predict_with_artifacts(image, filename=file.filename)
        
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
    return predictor.get_model_info()

@router.get("/predictions")
async def list_predictions():
    """Liste les prédictions effectuées"""
    import os
    predictions_dir = "predictions"
    
    if not os.path.exists(predictions_dir):
        return {"predictions": []}
    
    predictions = []
    for folder in sorted(os.listdir(predictions_dir), reverse=True):
        if folder.endswith("-result"):
            folder_path = os.path.join(predictions_dir, folder)
            result_file = os.path.join(folder_path, "prediction_result.json")
            
            if os.path.exists(result_file):
                with open(result_file, 'r') as f:
                    data = json.load(f)
                predictions.append({
                    "timestamp": data.get("timestamp"),
                    "filename": data.get("filename"),
                    "dominant_class": data.get("dominant_class"),
                    "dominant_class_percentage": data.get("dominant_class_percentage"),
                    "folder": folder
                })
    
    return {"predictions": predictions[:20]}  # Dernières 20 prédictions