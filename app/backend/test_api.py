# app/fastapi/test_api.py
import requests
import json
from PIL import Image
import io

def test_predict():
    """Test de l'endpoint de prédiction"""
    # URL de l'API
    url = "http://localhost:8000/api/v1/segmentation/predict"
    
    # Créer une image de test (ou charger une vraie image)
    test_image = Image.new('RGB', (224, 224), color='red')
    
    # Convertir en bytes
    img_bytes = io.BytesIO()
    test_image.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    # Envoyer la requête
    files = {'file': ('test.png', img_bytes, 'image/png')}
    response = requests.post(url, files=files)
    
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_predict()