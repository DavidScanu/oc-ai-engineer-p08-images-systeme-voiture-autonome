# app/backend/models/predictor.py
import os
import json
import numpy as np
import tensorflow as tf
import keras
import mlflow
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Any, Tuple, Optional, List
import logging
import tempfile
import shutil
import base64
import io
from datetime import datetime

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
        self.predictions_dir = "predictions"
        os.makedirs(self.predictions_dir, exist_ok=True)
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
    
    def image_to_base64(self, image: Image.Image) -> str:
        """Convertit une image PIL en base64"""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    
    def create_colored_mask(self, mask: np.ndarray) -> np.ndarray:
        """Crée un masque coloré à partir du masque de prédiction"""
        colored_mask = np.zeros((*mask.shape, 3), dtype=np.uint8)
        
        for class_id in range(settings.NUM_CLASSES):
            mask_for_class = (mask == class_id)
            colored_mask[mask_for_class] = settings.GROUP_COLORS[class_id]
        
        return colored_mask
    
    def create_overlay_visualization(self, original_img: Image.Image, colored_mask: np.ndarray) -> Image.Image:
        """Crée une superposition semi-transparente du masque sur l'image originale"""
        # Convertir l'image originale en array numpy
        original_array = np.array(original_img)
        
        # Redimensionner le masque si nécessaire
        if colored_mask.shape[:2] != original_array.shape[:2]:
            mask_img = Image.fromarray(colored_mask)
            mask_img = mask_img.resize(original_img.size, Image.NEAREST)
            colored_mask = np.array(mask_img)
        
        # Créer la superposition avec transparence
        alpha = 0.5
        overlay = original_array.copy()
        
        # Appliquer le masque coloré avec transparence (version numpy)
        overlay = (1 - alpha) * original_array + alpha * colored_mask
        overlay = overlay.astype(np.uint8)
        
        # Convertir en image PIL
        return Image.fromarray(overlay)
    
    def create_side_by_side_visualization(self, original_img: Image.Image, mask_img: Image.Image, 
                                         class_stats: List[Dict]) -> Image.Image:
        """Crée une visualisation avec l'image originale et la prédiction côte à côte"""
        # Dimensions
        width, height = original_img.size
        margin = 20
        text_height = 200  # Espace pour les statistiques
        
        # Créer une nouvelle image pour la visualisation
        total_width = width * 2 + margin * 3
        total_height = height + margin * 2 + text_height
        
        viz_img = Image.new('RGB', (total_width, total_height), color='white')
        
        # Coller l'image originale
        viz_img.paste(original_img, (margin, margin))
        
        # Coller le masque de prédiction
        viz_img.paste(mask_img, (width + margin * 2, margin))
        
        # Ajouter des labels
        draw = ImageDraw.Draw(viz_img)
        
        # Utiliser la police par défaut
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        except:
            font = ImageFont.load_default()
            small_font = font
        
        # Titres
        draw.text((margin, height + margin + 10), "Original", fill='black', font=font)
        draw.text((width + margin * 2, height + margin + 10), "Prédiction", fill='black', font=font)
        
        # Ajouter les statistiques
        y_offset = height + margin + 50
        draw.text((margin, y_offset), "Distribution des classes:", fill='black', font=small_font)
        
        y_offset += 25
        for i, stat in enumerate(class_stats[:5]):  # Top 5 classes
            text = f"{stat['class_name']}: {stat['percentage']:.1f}%"
            draw.text((margin, y_offset + i * 20), text, fill='black', font=small_font)
        
        return viz_img
    
    def predict_with_artifacts(self, image: Image.Image, filename: str = "image.png") -> Dict[str, Any]:
        """Effectue la prédiction et génère tous les artefacts"""
        if not self._model_loaded or self.model is None:
            raise RuntimeError("Le modèle n'est pas chargé correctement")
        
        try:
            # Créer le dossier de résultats avec timestamp
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            result_dir = os.path.join(self.predictions_dir, f"{timestamp}-result")
            os.makedirs(result_dir, exist_ok=True)
            
            # Sauvegarder l'image originale
            original_path = os.path.join(result_dir, "original.png")
            image.save(original_path)
            
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
            
            # Redimensionner à la taille originale
            original_size = image.size
            if pred_colored.shape[:2] != (original_size[1], original_size[0]):
                mask_img = Image.fromarray(pred_colored)
                mask_img = mask_img.resize(original_size, Image.NEAREST)
                pred_colored = np.array(mask_img)
            else:
                mask_img = Image.fromarray(pred_colored)
            
            # Sauvegarder le masque
            mask_path = os.path.join(result_dir, "prediction_mask.png")
            mask_img.save(mask_path)
            
            # Créer les visualisations
            overlay_img = self.create_overlay_visualization(image, pred_colored)
            overlay_path = os.path.join(result_dir, "visualization_overlay.png")
            overlay_img.save(overlay_path)
            
            side_by_side_img = self.create_side_by_side_visualization(image, mask_img, class_stats)
            side_by_side_path = os.path.join(result_dir, "visualization_side_by_side.png")
            side_by_side_img.save(side_by_side_path)
            
            # Préparer les résultats
            result_light = {
                'class_statistics': class_stats,
                'image_size': list(image.size),
                'segmented_image_size': list(pred_mask.shape),
                'num_classes': settings.NUM_CLASSES,
                'dominant_class': class_stats[0]['class_name'] if class_stats else '',
                'dominant_class_percentage': class_stats[0]['percentage'] if class_stats else 0.0,
                'timestamp': timestamp,
                'filename': filename
            }
            
            result_full = {
                **result_light,
                'prediction_mask': pred_mask.tolist(),
                'colored_mask': pred_colored.tolist()
            }
            
            # Sauvegarder les JSON
            with open(os.path.join(result_dir, "prediction_result.json"), "w") as f:
                json.dump(result_light, f, indent=2)
            
            with open(os.path.join(result_dir, "prediction_result_full.json"), "w") as f:
                json.dump(result_full, f, indent=2)
            
            # Préparer la réponse avec les images en base64
            response = {
                **result_light,
                'images': {
                    'original': self.image_to_base64(image),
                    'prediction_mask': self.image_to_base64(mask_img),
                    'overlay': self.image_to_base64(overlay_img),
                    'side_by_side': self.image_to_base64(side_by_side_img)
                },
                'artifacts_path': result_dir
            }
            
            logger.info(f"Prédiction terminée. Classe dominante: {class_stats[0]['class_name']} ({class_stats[0]['percentage']:.1f}%)")
            logger.info(f"Artefacts sauvegardés dans: {result_dir}")
            
            return response
            
        except Exception as e:
            logger.error(f"Erreur lors de la prédiction: {str(e)}")
            raise
    
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