
# Rapport d'Évaluation - Modèle de Segmentation Sémantique

## 🏷️ Identification de l'Expérience
- **Nom de l'expérience**: exp_001_baseline
- **Description**: Baseline MobileNetV2-UNet avec frozen encoder
- **Date d'évaluation**: 2025-05-23 11:40:11

## ⚙️ Configuration du Modèle
- **Architecture**: MobileNetV2-UNet
- **Backbone**: MobileNetV2 (ImageNet pré-entraîné)
- **Encoder trainable**: False
- **Classes de segmentation**: 8 groupes
- **Groupes de classes**: flat, human, vehicle, construction, object, nature, sky, void

## 📋 Paramètres d'Entraînement
- **Taille d'image**: (224, 224)
- **Batch size**: 8
- **Époques d'entraînement**: N/A
- **Taux d'apprentissage**: 0.0001
- **Division validation**: 0.2
- **Augmentation de données**: True

## 📊 Performances Finales sur Dataset de Test
- **Perte finale**: 0.4123
- **Précision finale**: 0.8795
- **MeanIoU finale**: 0.6325

## 🎯 Dataset et Évaluation
- **Dataset**: Cityscapes (segmentation urbaine)
- **Split utilisé pour test**: Dataset 'val' original (évite data leakage)
- **Nombre d'images de test**: ~500 images
- **Méthode d'évaluation**: IoU par classe, précision globale, matrice de confusion

## 📈 Mapping des Classes
Les 30+ classes originales de Cityscapes ont été regroupées en 8 catégories pertinentes 
pour la navigation autonome:

1. **Flat** (0): Routes, trottoirs, parkings
2. **Human** (1): Personnes, cyclistes  
3. **Vehicle** (2): Voitures, camions, bus, motos, vélos
4. **Construction** (3): Bâtiments, murs, clôtures, ponts
5. **Object** (4): Poteaux, panneaux, feux de circulation
6. **Nature** (5): Végétation, terrain
7. **Sky** (6): Ciel
8. **Void** (7): Pixels non étiquetés ou hors région d'intérêt

## 🚗 Applications et Déploiement
- **Cas d'usage**: Système de vision pour véhicules autonomes
- **Format de modèle**: Keras (.keras) - compatible TensorFlow Lite
- **Optimisations**: MobileNetV2 conçu pour l'efficacité mobile
- **Intégration**: API FastAPI + Frontend Next.js (en développement)

## 📂 Artefacts Générés
- **Modèle entraîné**: `experiments/exp_001_baseline/models/final_model.keras`
- **Configuration**: `experiments/exp_001_baseline/results/experiment_config.json`
- **Historique d'entraînement**: `experiments/exp_001_baseline/results/training_history.json`
- **Métriques détaillées**: `experiments/exp_001_baseline/results/`
- **Visualisations**: Matrice de confusion, exemples de prédictions

## 🔄 Suivi et Reproductibilité
- **Structure d'expériences**: Organisation modulaire par dossiers
- **Intégration MLflow**: Suivi des métriques et artefacts
- **Graine aléatoire**: 42 (reproductibilité garantie)
- **Environnement**: TensorFlow 2.18.0, Keras 3.8.0

## 📝 Notes Techniques
- Le modèle utilise SparseCategoricalCrossentropy comme fonction de perte
- L'encoder MobileNetV2 peut être gelé ou entraînable selon la configuration
- La segmentation est réalisée à 224x224 puis peut être redimensionnée
- L'augmentation de données inclut flip horizontal et variation de luminosité

## 🎯 Recommandations
1. **Pour améliorer les performances**: Considérer l'entraînement avec encoder dégelé
2. **Pour le déploiement**: Conversion en TensorFlow Lite pour l'optimisation mobile
3. **Pour l'évaluation**: Utiliser des métriques IoU par classe pour l'analyse détaillée
4. **Pour la production**: Implémenter une validation croisée sur plusieurs datasets urbains

---
*Rapport généré automatiquement le 2025-05-23 à 11:40:11*
