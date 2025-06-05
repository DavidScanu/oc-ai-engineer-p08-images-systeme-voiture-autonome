# app/fastapi/models/predictor.py
import os
import json
import numpy as np
import tensorflow as tf
import keras  # Import direct pour Keras 3.x
import mlflow
from PIL import Image
from typing import Dict, Any, Tuple, Optional
import logging
import tempfile
import shutil

from config import settings

# Configuration de MLflow
os.environ["AWS_ACCESS_KEY_ID"] = settings.AWS_ACCESS_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"] = settings.AWS_SECRET_ACCESS_KEY
mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

logger = logging.getLogger(__name__)

class SegmentationPredictor:
    def __init__(self):
        self.model: Optional[keras.Model] = None
        self.class_mapping: Optional[Dict[str, Any]] = None
        self.id_to_group: Optional[np.ndarray] = None
        self._model_loaded = False
        self.load_model()
    
    def load_model(self):
        """Charge le modèle et la configuration depuis MLflow"""
        try:
            logger.info(f"Chargement du modèle depuis MLflow run_id: {settings.RUN_ID}")
            
            # Créer un client MLflow
            client = mlflow.MlflowClient()
            
            # Créer un répertoire temporaire pour télécharger les artefacts
            with tempfile.TemporaryDirectory() as temp_dir:
                # Télécharger le modèle complet
                model_path = client.download_artifacts(
                    settings.RUN_ID, 
                    "model",
                    dst_path=temp_dir
                )
                
                # Le modèle Keras devrait être dans model/data/model.keras
                keras_model_path = os.path.join(model_path, "data", "model.keras")
                
                if not os.path.exists(keras_model_path):
                    # Essayer d'autres chemins possibles
                    keras_model_path = os.path.join(model_path, "model.keras")
                    if not os.path.exists(keras_model_path):
                        # Chercher le fichier .keras dans le répertoire
                        for root, dirs, files in os.walk(model_path):
                            for file in files:
                                if file.endswith('.keras'):
                                    keras_model_path = os.path.join(root, file)
                                    break
                
                logger.info(f"Chargement du modèle depuis: {keras_model_path}")
                
                # Charger le modèle avec Keras 3.x
                self.model = keras.saving.load_model(keras_model_path, compile=False)
                
                # Recompiler le modèle avec les métriques appropriées
                self.model.compile(
                    optimizer=keras.optimizers.Adam(learning_rate=0.0001),
                    loss=keras.losses.SparseCategoricalCrossentropy(),
                    metrics=[keras.metrics.SparseCategoricalAccuracy()]
                )
                
                logger.info("Modèle chargé et compilé avec succès")
                
                # Télécharger le mapping des classes
                mapping_path = client.download_artifacts(
                    settings.RUN_ID, 
                    "class_mapping.json",
                    dst_path=temp_dir
                )
                
                # Lire le fichier JSON
                with open(mapping_path, 'r') as f:
                    self.class_mapping = json.load(f)
                
                # Reconstruire id_to_group
                self.id_to_group = np.array(self.class_mapping['id_to_group'], dtype=np.uint8)
                
                self._model_loaded = True
                logger.info("Configuration chargée avec succès")
                
                # Afficher les informations du modèle
                logger.info(f"Modèle: {self.model.name}")
                logger.info(f"Input shape: {self.model.input_shape}")
                logger.info(f"Output shape: {self.model.output_shape}")
                logger.info(f"Nombre de paramètres: {self.model.count_params():,}")
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle: {str(e)}")
            logger.error(f"Type d'erreur: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback complet:\n{traceback.format_exc()}")
            self._model_loaded = False
            raise
    
    def preprocess_image(self, image: Image.Image) -> tf.Tensor:
        """Préprocesse l'image pour la prédiction"""
        try:
            # Convertir en RGB si nécessaire
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convertir en numpy array
            img_array = np.array(image, dtype=np.float32)
            
            # Redimensionner avec TensorFlow
            img_resized = tf.image.resize(
                img_array, 
                settings.IMG_SIZE, 
                method=tf.image.ResizeMethod.BILINEAR,
                antialias=True
            )
            
            # Normaliser [0,1]
            img_normalized = img_resized / 255.0
            
            # Ajouter dimension batch
            img_batch = tf.expand_dims(img_normalized, axis=0)
            
            # S'assurer que le tensor a la bonne forme
            img_batch = tf.ensure_shape(img_batch, [1, settings.IMG_SIZE[0], settings.IMG_SIZE[1], 3])
            
            return img_batch
            
        except Exception as e:
            logger.error(f"Erreur lors du préprocessing de l'image: {str(e)}")
            raise
    
    def predict(self, image: Image.Image) -> Dict[str, Any]:
        """Effectue la prédiction sur une image"""
        if not self._model_loaded or self.model is None:
            raise RuntimeError("Le modèle n'est pas chargé correctement")
        
        try:
            # Préprocesser l'image
            img_tensor = self.preprocess_image(image)
            
            logger.info(f"Forme du tensor d'entrée: {img_tensor.shape}")
            
            # Faire la prédiction
            predictions = self.model.predict(img_tensor, verbose=0)
            
            logger.info(f"Forme des prédictions: {predictions.shape}")
            
            # Convertir en masque de classes
            pred_mask = tf.argmax(predictions, axis=-1)[0].numpy()
            
            # Calculer les statistiques
            unique_classes, counts = np.unique(pred_mask, return_counts=True)
            total_pixels = pred_mask.size
            
            class_stats = []
            for class_id in range(settings.NUM_CLASSES):
                if class_id in unique_classes:
                    idx = np.where(unique_classes == class_id)[0][0]
                    count = counts[idx]
                else:
                    count = 0
                
                class_name = settings.GROUP_NAMES[class_id]
                percentage = (count / total_pixels) * 100
                
                class_stats.append({
                    'class_id': int(class_id),
                    'class_name': class_name,
                    'pixel_count': int(count),
                    'percentage': float(percentage)
                })
            
            # Trier par pourcentage décroissant
            class_stats.sort(key=lambda x: x['percentage'], reverse=True)
            
            # Créer le masque coloré
            pred_colored = self.create_colored_mask(pred_mask)
            
            # Log des statistiques principales
            logger.info(f"Prédiction terminée. Classe dominante: {class_stats[0]['class_name']} ({class_stats[0]['percentage']:.1f}%)")
            
            return {
                'prediction_mask': pred_mask.tolist(),
                'colored_mask': pred_colored.tolist(),
                'class_statistics': class_stats,
                'image_size': list(pred_mask.shape),
                'num_classes': settings.NUM_CLASSES
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la prédiction: {str(e)}")
            raise
    
    def create_colored_mask(self, mask: np.ndarray) -> np.ndarray:
        """Crée un masque coloré à partir du masque de prédiction"""
        colored_mask = np.zeros((*mask.shape, 3), dtype=np.uint8)
        
        for class_id in range(settings.NUM_CLASSES):
            mask_for_class = (mask == class_id)
            colored_mask[mask_for_class] = settings.GROUP_COLORS[class_id]
        
        return colored_mask
    
    def get_model_info(self) -> Dict[str, Any]:
        """Retourne les informations sur le modèle"""
        if not self._model_loaded or self.model is None:
            return {
                "status": "Model not loaded",
                "model_loaded": False
            }
        
        return {
            "status": "Model loaded successfully",
            "model_loaded": True,
            "model_name": self.model.name if hasattr(self.model, 'name') else "MobileNetV2-UNet",
            "input_shape": list(self.model.input_shape),
            "output_shape": list(self.model.output_shape),
            "num_parameters": int(self.model.count_params()),
            "num_classes": settings.NUM_CLASSES,
            "class_names": settings.GROUP_NAMES,
            "class_colors": settings.GROUP_COLORS,
            "tensorflow_version": tf.__version__,
            "keras_version": keras.__version__
        }

# Instance globale du prédicteur
try:
    predictor = SegmentationPredictor()
    logger.info("Prédicteur initialisé avec succès")
except Exception as e:
    logger.error(f"Erreur lors de l'initialisation du prédicteur: {str(e)}")
    predictor = None