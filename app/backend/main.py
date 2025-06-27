# app/backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

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

# Configuration CORS pour Heroku
origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    os.getenv("FRONTEND_URL", "*"),  # URL de votre frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
        "status": "running on Heroku" if settings.IS_HEROKU else "running locally",
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
    logger.info(f"Running on Heroku: {settings.IS_HEROKU}")
    logger.info(f"Port: {settings.PORT}")
    logger.info(f"MLflow tracking URI: {settings.MLFLOW_TRACKING_URI}")
    logger.info(f"Run ID: {settings.RUN_ID}")
