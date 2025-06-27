# Backend : FastAPI

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```



## Déploiement 

Vous n'avez pas npm installé. Mettons à jour Heroku CLI avec la méthode appropriée pour votre système :

## Mise à jour de Heroku CLI sur Linux

### Option 1 : Via apt (Ubuntu/Debian)

```bash
# Mettre à jour Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Ou si vous l'avez installé via apt
sudo apt update
sudo apt upgrade heroku
```

### Vérifier la version actuelle

```bash
heroku --version
```

## Vérifier votre compte Heroku

```bash
# Se reconnecter
heroku login

# Lister vos apps
heroku apps
```

### Créer une nouvelle application

Créons une nouvelle app :

```bash
# Créer une nouvelle app
heroku create cityscapes-api-v2 --region eu

# Configurer les variables d'environnement
heroku config:set \
  MLFLOW_TRACKING_URI="MLFLOW_TRACKING_URI" \
  AWS_ACCESS_KEY_ID="AWS_ACCESS_KEY_ID" \
  AWS_SECRET_ACCESS_KEY="AWS_SECRET_ACCESS_KEY" \
  RUN_ID="RUN_ID" \
  -a cityscapes-api-v2

# Ajouter le nouveau remote
heroku git:remote -a cityscapes-api-v2

# Déployer
git subtree push --prefix app/backend heroku main
```
