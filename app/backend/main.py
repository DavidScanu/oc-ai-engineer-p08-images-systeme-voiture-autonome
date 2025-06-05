# app/fastapi/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from routers import segmentation
from config import settings

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Créer l'application FastAPI
app = FastAPI(
    title="Cityscapes Segmentation API",
    description="API pour la segmentation sémantique d'images urbaines",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(
    segmentation.router,
    prefix="/api/v1/segmentation",
    tags=["segmentation"]
)

@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "message": "API de segmentation sémantique Cityscapes",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/api/v1/segmentation/predict",
            "health": "/api/v1/segmentation/health",
            "model_info": "/api/v1/segmentation/model/info"
        }
    }

@app.on_event("startup")
async def startup_event():
    """Événement au démarrage de l'application"""
    logger.info("Démarrage de l'API...")
    logger.info(f"MLflow tracking URI: {settings.MLFLOW_TRACKING_URI}")
    logger.info(f"Run ID: {settings.RUN_ID}")