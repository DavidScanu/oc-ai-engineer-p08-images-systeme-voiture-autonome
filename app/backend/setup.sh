#!/bin/bash
# Script de configuration pour l'API FastAPI

echo "🔧 Configuration de l'environnement pour l'API FastAPI"

# Créer l'environnement virtuel
echo "📦 Création de l'environnement virtuel..."
python -m venv .venv

# Activer l'environnement
echo "🚀 Activation de l'environnement..."
source .venv/bin/activate

# Mettre à jour pip
echo "📥 Mise à jour de pip..."
pip install --upgrade pip

# Installer les dépendances
echo "📚 Installation des dépendances..."
pip install -r requirements.txt

echo "✅ Installation terminée!"
echo "🎯 Pour lancer l'API: uvicorn main:app --reload"