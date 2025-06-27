# Backend : FastAPI

## Lancer l'API en local

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

```bash
gunicorn main:app -k uvicorn.workers.UvicornWorker --workers 1 --threads 1 --bind 0.0.0.0:8000 --timeout 120
```

## lancer l'API sur un serveur distant

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