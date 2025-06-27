# Backend : FastAPI

Lancement en local : 

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

```bash
gunicorn main:app -k uvicorn.workers.UvicornWorker --workers 1 --threads 1 --bind 0.0.0.0:8000 --timeout 120
```

Lancement sur le serveur (déploiement) : 

```bash
uvicorn main:app --reload --host 0.0.0.0 --port ${PORT:-8000}
```

````bash
web: gunicorn main:app -k uvicorn.workers.UvicornWorker --workers 1 --threads 4 --bind 0.0.0.0:$PORT --timeout 120
```
