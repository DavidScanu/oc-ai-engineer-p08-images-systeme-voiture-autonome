# 🚗 Projet 8 : Traitement d'images pour le système embarqué d'une voiture autonome

![TensorFlow](https://img.shields.io/badge/TensorFlow-2.19-FF6F00?logo=tensorflow&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-async%20API-009688?logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-frontend-000000?logo=next.js&logoColor=white)
[![Pytest](https://img.shields.io/github/actions/workflow/status/DavidScanu/oc-ai-engineer-p08-systeme-voiture-autonome/heroku-deploy.yml?label=pytest&logo=pytest&logoColor=white)](https://github.com/DavidScanu/oc-ai-engineer-p08-systeme-voiture-autonome/actions/workflows/heroku-deploy.yml)
[![Deploy to Heroku](https://github.com/DavidScanu/oc-ai-engineer-p08-systeme-voiture-autonome/actions/workflows/heroku-deploy.yml/badge.svg)](https://github.com/DavidScanu/oc-ai-engineer-p08-systeme-voiture-autonome/actions/workflows/heroku-deploy.yml)

> 🎓 OpenClassrooms • Parcours [AI Engineer](https://openclassrooms.com/fr/paths/795-ai-engineer) | 👋 *Étudiant* : [David Scanu](https://www.linkedin.com/in/davidscanu14/)

## 📋 Table des matières
- [Contexte](#-contexte)
- [Mission](#-mission)
- [Objectifs pédagogiques](#-objectifs-pédagogiques)
- [Plan de travail](#-plan-de-travail)
- [Livrables](#-livrables)
- [Technologies utilisées](#-technologies-utilisées)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Démonstration](#-démonstration)
- [Résultats](#-résultats)

## 🌐 Contexte
Ce projet s'inscrit dans le développement d'un **système embarqué de vision par ordinateur** pour véhicules autonomes chez **Future Vision Transport**. L'entreprise conçoit des systèmes permettant aux véhicules autonomes de percevoir leur environnement grâce à l'analyse d'images en temps réel.

## ⚡ Mission
En tant qu'ingénieur IA dans l'équipe R&D, notre mission est de **développer le module de segmentation d'images** (composant 3) qui s'intègre entre le module de traitement d'images (2) et le système de décision (4). Ce module doit être capable d'**identifier et de segmenter précisément 8 catégories principales d'objets** dans des images de caméras embarquées.

## 🎯 Objectifs pédagogiques
- Développer un modèle de segmentation d'images performant avec Keras/TensorFlow
- Concevoir et déployer une API REST avec FastAPI
- Créer une application web de démonstration avec Next.js
- Mettre en place un pipeline d'entraînement et de déploiement complet
- Évaluer et améliorer les performances du modèle
- Documenter le processus et les résultats de façon claire et professionnelle

## 🗓️ Plan de travail

1. **Exploration et préparation des données**
   - Analyse du jeu de données fourni par Franck (images et masques segmentés)
   - Prétraitement et augmentation des données
   - Création d'un générateur de données optimisé

2. **Développement du modèle de segmentation**
   - Étude des architectures de l'état de l'art (U-Net, DeepLabV3+, etc.)
   - Implémentation avec Keras
   - Entraînement et optimisation du modèle

3. **Déploiement du modèle**
   - Développement d'une API FastAPI
   - Création d'une application frontend Next.js
   - Déploiement sur Heroku

4. **Évaluation et documentation**
   - Tests et validation des performances
   - Rédaction du rapport technique
   - Préparation de la présentation

## 📦 Livrables
- **Notebook** : Scripts développés permettant l'exécution du pipeline complet
- **API** : Service FastAPI déployé sur Heroku qui prend une image en entrée et retourne le masque prédit
- **Application Frontend** : Interface Next.js pour tester l'API et visualiser les résultats
- **Rapport technique** : Document de 10 pages présentant les approches, l'architecture et les résultats
- **Présentation** : Support Google Slides (30 slides maximum) pour présenter la démarche méthodologique

## 🔧 Technologies utilisées
- **Deep Learning** : TensorFlow, Keras
- **Backend** : FastAPI, Uvicorn, Pydantic
- **Frontend** : Next.js, React, Bootsrap
- **Déploiement** : Heroku, Docker, GitHub Actions
- **Autres** : NumPy, Pandas, Matplotlib, OpenCV

## 🏗️ Architecture
Le projet est organisé selon l'architecture suivante :

```
├── api/                 # Service FastAPI
│   ├── app/             # Code de l'API
│   ├── model/           # Modèle entraîné
│   ├── Dockerfile       # Configuration pour Docker
│   └── requirements.txt # Dépendances Python
├── frontend/            # Application Next.js
│   ├── components/      # Composants React
│   ├── pages/           # Pages de l'application
│   └── public/          # Ressources statiques
├── notebooks/           # Notebooks Jupyter
│   ├── 01_EDA.ipynb     # Exploration des données
│   ├── 02_Model.ipynb   # Développement du modèle
│   └── 03_Evaluation.ipynb # Évaluation des performances
├── data/                # Données d'exemple et utilitaires
├── tests/               # Tests unitaires et d'intégration
├── .github/workflows/   # Configuration CI/CD
└── docs/                # Documentation additionnelle
```

## 🚀 Installation

### Prérequis
- Python 3.9+
- Node.js 16+
- npm ou yarn

### API (Backend)
```bash
# Cloner le dépôt
git clone https://github.com/DavidScanu/oc-ai-engineer-p08-systeme-voiture-autonome.git
cd oc-ai-engineer-p08-systeme-voiture-autonome/api

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'API en local
uvicorn app.main:app --reload
```

### Frontend
```bash
cd ../frontend

# Installer les dépendances
npm install

# Lancer l'application en développement
npm run dev
```

## 🌐 Démonstration

- **API** : [https://oc-p8-segmentation-api.herokuapp.com/docs](https://oc-p8-segmentation-api.herokuapp.com/docs)
- **Frontend** : [https://oc-p8-segmentation-frontend.herokuapp.com](https://oc-p8-segmentation-frontend.herokuapp.com)

## 📊 Résultats

Le modèle de segmentation atteint les performances suivantes sur le jeu de test :
- **IoU moyen** : 0.85
- **Précision** : 0.92
- **Recall** : 0.89

Ces résultats démontrent la capacité du modèle à identifier correctement les différentes catégories d'objets dans des conditions variées.

## 📜 Licence

Ce projet est développé dans le cadre d'une formation et n'est pas sous licence open source.

## 👨‍💻 À propos

Projet développé par [David Scanu](https://www.linkedin.com/in/davidscanu14/) dans le cadre du parcours [AI Engineer](https://openclassrooms.com/fr/paths/795-ai-engineer) d'OpenClassrooms : *Projet 8 - **Traitez les images pour le système embarqué d'une voiture autonome*.
