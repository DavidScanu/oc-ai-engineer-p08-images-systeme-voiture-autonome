# 📊 API de Prédiction Sémantique Future Vision Transport (FastAPI)

Cette API permet de réaliser la **segmentation sémantique d’images urbaines** pour véhicules autonomes, basée sur un modèle Deep Learning entraîné sur Cityscapes. L'API est développée avec **FastAPI** et utilise **TensorFlow/Keras** pour la segmentation sémantique.

Elle expose plusieurs endpoints pour prédire, obtenir des informations sur le modèle, vérifier la santé du service et lister les prédictions réalisées.

---

### **Endpoints principaux**

#### `POST /api/v1/segmentation/predict`
- **Description :**  
  Prédit la segmentation sémantique d’une image envoyée (JPEG, PNG, etc.). Retourne les masques, visualisations et statistiques.
- **Paramètres :**  
  - `file` (form-data, obligatoire) : image à segmenter.
- **Réponse :**
  ```json
  {
    "class_statistics": [
      {"class_id": 0, "class_name": "flat", "pixel_count": 12345, "percentage": 45.6},
      ...
    ],
    "dominant_class": "flat",
    "dominant_class_percentage": 45.6,
    "image_size": [224, 224],
    "images": {
      "original": "<base64>",
      "prediction_mask": "<base64>",
      "overlay": "<base64>",
      "side_by_side": "<base64>"
    }
  }
  ```

#### `GET /api/v1/segmentation/health`

- **Description :**  
  Vérifie la santé de l’API et si le modèle est chargé.
- **Réponse :**
  ```json
  {
    "status": "healthy",
    "model_loaded": true
  }
  ```


#### `GET /api/v1/segmentation/model/info`

- **Description :**  
  Retourne les informations sur le modèle chargé (nom, shape, classes, couleurs, version TensorFlow/Keras, etc.).
- **Réponse :**
  ```json
  {
    "status": "Model loaded successfully",
    "model_loaded": true,
    "model_name": "MobileNetV2-UNet",
    "input_shape": [null, 224, 224, 3],
    "output_shape": [null, 224, 224, 8],
    "num_parameters": 5418600,
    "num_classes": 8,
    "class_names": ["flat", "human", ...],
    "class_colors": [[128,64,128], ...],
    "tensorflow_version": "2.18.0",
    "keras_version": "3.8.0"
  }
  ```

#### `GET /api/v1/segmentation/predictions`
- **Description :**  
  Liste les dernières prédictions effectuées (timestamp, nom du fichier, classe dominante, etc.).
- **Réponse :**
  ```json
  {
    "predictions": [
      {
        "timestamp": "20240627-153000",
        "filename": "image.png",
        "dominant_class": "flat",
        "dominant_class_percentage": 45.6,
        "folder": "20240627-153000-result"
      },
      ...
    ]
  }
  ```

### **Résumé**

- **Upload d’image** → segmentation sémantique instantanée.
- **Statistiques détaillées** sur les classes détectées.
- **Visualisations** (masque, overlay, côte à côte) en base64.
- **Endpoints de monitoring** pour la santé et l’info modèle.
- **Historique des prédictions** accessible.

---



## Lancement de l'API

### En local (développement et production)

Comment démarrer l’API en local :

- Utilisez la commande `uvicorn` pour le développement, avec rechargement automatique.
- Utilisez la commande `gunicorn` (avec worker Uvicorn) pour un lancement en mode production ou pré-production.

Ces instructions vous permettent de tester ou déployer rapidement l’API sur votre machine.

#### En local (développement)

Pour démarrer l'API en mode développement, utilisez la commande suivante :

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### En local (production)

Pour démarrer l'API en mode production, utilisez Gunicorn avec Uvicorn comme worker :

```bash
gunicorn main:app -k uvicorn.workers.UvicornWorker --workers 1 --threads 1 --bind 0.0.0.0:8000 --timeout 120
```

## Sur un serveur distant

Pour déployer l'API sur un serveur distant, vous pouvez utiliser les commandes suivantes :

```bash
uvicorn main:app --reload --host 0.0.0.0 --port ${PORT:-8000}
```

```bash
web: gunicorn main:app -k uvicorn.workers.UvicornWorker --workers 1 --threads 4 --bind 0.0.0.0:$PORT --timeout 120
```

## Déploiement sur Railway : Méthode complète via Dashboard (Recommandée)

1. **Ouvrir le dashboard** :
   ```bash
   railway open
   ```

2. **Dans le navigateur** :
   - Créer un service si nécessaire
   - Configurer les variables d'environnement
   - Dans l'onglet "Settings" du service :
     - Root Directory: `/` (puisque vous êtes déjà dans app/backend)
     - Watch Patterns: laissez par défaut

3. **Déployer depuis la CLI** :

### Installation de la CLI Railway

Pour déployer l'API de segmentation sémantique sur Railway, suivez ces étapes :

1. **Connexion à Railway** :
   ```bash
   railway login
   ```

2. **Initialiser le projet Railway** :
   ```bash
   railway init
   ```

3. **Créer un service (si nécessaire)** :
   ```bash
   railway service create
   ```

4. **Lier le projet local au projet Railway** :
   ```bash
   railway link
   ```

5. **Déployer le projet** :
   ```bash
   railway up
   ```

4. **Ou connecter GitHub** (pour déploiements automatiques) :
   - Dans Settings → GitHub Repo
   - Connectez votre repo
   - Set Root Directory to: `app/backend`
   - Railway déploiera automatiquement à chaque push

## Vérification

```bash
# Vérifier que tout est configuré
railway status

# Voir les logs
railway logs

# Voir les variables (lecture seule)
railway variables
```

La clé est de configurer les variables via le dashboard web avant de déployer, car la CLI semble avoir des limitations pour définir les variables directement.