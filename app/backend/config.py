# app/fastapi/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    RUN_ID = os.getenv("RUN_ID")
    MODEL_NAME = "cityscapes_segmentation"
    IMG_SIZE = (224, 224)
    NUM_CLASSES = 8
    
    # Noms et couleurs des classes
    GROUP_NAMES = ['flat', 'human', 'vehicle', 'construction', 'object', 'nature', 'sky', 'void']
    GROUP_COLORS = [
        [128, 64, 128],  # flat - bleu-gris
        [220, 20, 60],   # human - rouge
        [0, 0, 142],     # vehicle - bleu foncé
        [70, 70, 70],    # construction - gris
        [220, 220, 0],   # object - jaune
        [107, 142, 35],  # nature - vert
        [70, 130, 180],  # sky - bleu ciel
        [0, 0, 0]        # void - noir
    ]

settings = Settings()