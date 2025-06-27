# Frontend Segmentation avec Next.js

## Variables d'environnement

Avant de démarrer le projet, assurons-nous de configurer les variables d'environnement nécessaires. Nous devons définir dans un fichier `.env.local` les variables suivantes :

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1/segmentation
```

## Lancer l'interface utilisateur "Future Vison Transport" 

## 1. Lancer l'API FastAPI

Nous devons démarrer l'API de prédiction en mode développement avec la commande suivante :

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 2. Lancer l'interface utilisateur Next.js

Pour démarrer l'interface utilisateur Next.js, nous utilisons la commande suivante :

```bash
npm run dev
```

## 3. Pour accéder à l'application

Nous ouvrons notre navigateur et accédons à l'URL suivante :

```
http://localhost:3000
```

## Déploiement sur Vercel

Pour déployer l'application Next.js, nous pouvons utiliser la plateforme Vercel.

1. Rendez-vous sur [https://vercel.com/](https://vercel.com/) et nous nous connectons avec notre compte GitHub.
2. Nous cliquons sur **"New Project"** et importons le dépôt contenant notre projet Next.js.
3. Nous sélectionnons le dépôt, puis cliquons sur **"Import"**.
4. Nous configurons les variables d'environnement dans l'onglet **"Environment Variables"**
  - `NEXT_PUBLIC_API_URL` : URL de l'API de prédiction FastAPI (par exemple, `http://localhost:8000/api/v1/segmentation` pour le développement local ou l'URL de l'API déployée en production).
5. Nous cliquons sur **"Deploy"** pour lancer le déploiement.
6. Une fois le déploiement terminé, nous accedons à l'URL fournie par Vercel pour voir notre application en ligne.