# app/backend/test-prediction/test_prediction.py
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import io
import os
import numpy as np
from datetime import datetime
import shutil

def test_api():
    # Configuration
    base_url = "http://localhost:8000"
    
    # Créer le dossier results s'il n'existe pas
    os.makedirs("results", exist_ok=True)
    
    # 1. Test health
    print("🏥 Test Health Check...")
    response = requests.get(f"{base_url}/api/v1/segmentation/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    
    # 2. Test model info
    print("ℹ️ Test Model Info...")
    response = requests.get(f"{base_url}/api/v1/segmentation/model/info")
    print(f"Status: {response.status_code}")
    info = response.json()
    # Afficher les infos sans les couleurs (trop verbeux)
    info_filtered = {k: v for k, v in info.items() if k != 'class_colors'}
    print(f"Response: {json.dumps(info_filtered, indent=2)}\n")
    
    # Récupérer les couleurs des classes pour plus tard
    class_colors = info.get('class_colors', [])
    class_names = info.get('class_names', [])
    
    # 3. Test avec l'image Berlin
    print("🔮 Test Prediction avec berlin_000000_000019_leftImg8bit.png...")
    
    # Chemin de l'image
    image_path = "berlin_000000_000019_leftImg8bit.png"
    
    if not os.path.exists(image_path):
        print(f"❌ Image non trouvée: {image_path}")
        print("Assurez-vous d'exécuter le script depuis le dossier test-prediction/")
        return
    
    # Créer un dossier avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    result_dir = os.path.join("results", f"{timestamp}-prediction")
    os.makedirs(result_dir, exist_ok=True)
    print(f"📁 Dossier de résultats créé: {result_dir}")
    
    # Copier l'image originale
    shutil.copy2(image_path, os.path.join(result_dir, "original.png"))
    
    # Ouvrir et envoyer l'image
    with open(image_path, 'rb') as f:
        files = {'file': (image_path, f, 'image/png')}
        response = requests.post(
            f"{base_url}/api/v1/segmentation/predict",
            files=files
        )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        
        # Sauvegarder la réponse complète
        with open(os.path.join(result_dir, "prediction_result.json"), "w") as f:
            # Sauvegarder sans les masques pour réduire la taille
            result_light = {
                'class_statistics': result.get('class_statistics', []),
                'image_size': result.get('image_size', []),
                'num_classes': result.get('num_classes', 0)
            }
            json.dump(result_light, f, indent=2)
        print("✅ Résultat sauvegardé dans prediction_result.json (version allégée)")
        
        # Sauvegarder la version complète
        with open(os.path.join(result_dir, "prediction_result_full.json"), "w") as f:
            json.dump(result, f)
        print("✅ Résultat complet sauvegardé dans prediction_result_full.json")
        
        # Créer et sauvegarder l'image de prédiction
        if 'prediction_mask' in result and 'colored_mask' in result:
            create_prediction_images(
                result, 
                image_path, 
                result_dir, 
                class_colors, 
                class_names
            )
        
        # Afficher les statistiques
        print(f"\n📐 Taille de l'image segmentée: {result.get('image_size', 'N/A')}")
        print(f"🎨 Nombre de classes: {result.get('num_classes', 'N/A')}")
        
        # Statistiques des classes
        if 'class_statistics' in result:
            stats = result['class_statistics']
            
            # Classe dominante
            if stats:
                dominant = stats[0]
                print(f"\n🏆 Classe dominante: {dominant['class_name']} ({dominant['percentage']:.1f}%)")
            
            # Distribution complète
            print("\n📊 Distribution des classes:")
            print("-" * 60)
            for stat in stats:
                percentage = stat['percentage']
                pixels = stat['pixel_count']
                bar_length = int(percentage / 2)  # Max 50 caractères
                bar = '█' * bar_length
                print(f"{stat['class_name']:>12}: {bar:<50} {percentage:>5.1f}% ({pixels:,} pixels)")
            print("-" * 60)
            
            # Résumé
            total_pixels = sum(s['pixel_count'] for s in stats)
            print(f"\n📈 Total pixels analysés: {total_pixels:,}")
            
        # Info sur la taille de la réponse
        response_size = len(response.text)
        print(f"\n💾 Taille de la réponse complète: {response_size:,} octets ({response_size/1024/1024:.1f} MB)")
        
        print(f"\n✅ Tous les fichiers sauvegardés dans: {result_dir}")
        
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(f"Détails: {response.text}")

def create_prediction_images(result, original_image_path, output_dir, class_colors, class_names):
    """Crée et sauvegarde les images de prédiction"""
    print("\n🎨 Création des images de prédiction...")
    
    # Charger l'image originale
    original_img = Image.open(original_image_path)
    original_size = original_img.size
    
    # Récupérer les masques
    prediction_mask = np.array(result['prediction_mask'])
    colored_mask = np.array(result['colored_mask'], dtype=np.uint8)
    
    # Redimensionner les masques à la taille originale si nécessaire
    if prediction_mask.shape != (original_size[1], original_size[0]):
        # Créer une image PIL à partir du masque coloré
        colored_mask_img = Image.fromarray(colored_mask)
        # Redimensionner à la taille originale
        colored_mask_img = colored_mask_img.resize(original_size, Image.NEAREST)
        colored_mask = np.array(colored_mask_img)
    
    # Sauvegarder l'image du masque coloré
    mask_img = Image.fromarray(colored_mask)
    mask_path = os.path.join(output_dir, "prediction_mask.png")
    mask_img.save(mask_path)
    print(f"✅ Masque de prédiction sauvegardé: prediction_mask.png")
    
    # Créer une visualisation côte à côte
    create_side_by_side_visualization(
        original_img, 
        mask_img, 
        output_dir, 
        result.get('class_statistics', [])
    )
    
    # Créer une superposition semi-transparente
    create_overlay_visualization(
        original_img,
        colored_mask,
        output_dir
    )

def create_side_by_side_visualization(original_img, mask_img, output_dir, class_stats):
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
    
    # Essayer de charger une police, sinon utiliser la police par défaut
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
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
    
    # Sauvegarder
    viz_path = os.path.join(output_dir, "visualization_side_by_side.png")
    viz_img.save(viz_path)
    print(f"✅ Visualisation côte à côte sauvegardée: visualization_side_by_side.png")

def create_overlay_visualization(original_img, colored_mask, output_dir):
    """Crée une superposition semi-transparente du masque sur l'image originale"""
    
    # Convertir l'image originale en array numpy
    original_array = np.array(original_img)
    
    # Redimensionner si nécessaire
    if colored_mask.shape[:2] != original_array.shape[:2]:
        mask_img = Image.fromarray(colored_mask)
        mask_img = mask_img.resize(original_img.size, Image.NEAREST)
        colored_mask = np.array(mask_img)
    
    # Créer la superposition avec transparence
    alpha = 0.5
    overlay = original_array.copy()
    
    # Appliquer le masque coloré avec transparence
    overlay = cv2.addWeighted(original_array, 1-alpha, colored_mask, alpha, 0)
    
    # Convertir en image PIL et sauvegarder
    overlay_img = Image.fromarray(overlay)
    overlay_path = os.path.join(output_dir, "visualization_overlay.png")
    overlay_img.save(overlay_path)
    print(f"✅ Visualisation avec superposition sauvegardée: visualization_overlay.png")

def visualize_results():
    """Visualise les résultats sauvegardés"""
    print("\n📊 Visualisation des derniers résultats...")
    
    # Trouver le dernier dossier de résultats
    results_dir = "results"
    if not os.path.exists(results_dir):
        print("❌ Aucun dossier de résultats trouvé")
        return
    
    # Lister tous les dossiers de prédiction
    prediction_dirs = [d for d in os.listdir(results_dir) 
                      if os.path.isdir(os.path.join(results_dir, d)) and d.endswith('-prediction')]
    
    if not prediction_dirs:
        print("❌ Aucun résultat de prédiction trouvé")
        return
    
    # Prendre le plus récent
    latest_dir = sorted(prediction_dirs)[-1]
    latest_path = os.path.join(results_dir, latest_dir)
    
    print(f"📁 Analyse du dossier: {latest_dir}")
    
    # Lister les fichiers
    files = os.listdir(latest_path)
    print(f"\n📄 Fichiers trouvés:")
    for file in sorted(files):
        file_path = os.path.join(latest_path, file)
        size = os.path.getsize(file_path)
        print(f"  - {file:<35} ({size:,} octets)")
    
    # Charger et afficher les statistiques
    result_file = os.path.join(latest_path, "prediction_result.json")
    if os.path.exists(result_file):
        with open(result_file, "r") as f:
            data = json.load(f)
        
        if 'class_statistics' in data:
            stats = data['class_statistics']
            print(f"\n🎯 Classe dominante: {stats[0]['class_name']} ({stats[0]['percentage']:.1f}%)")

# Import cv2 seulement si disponible, sinon utiliser PIL uniquement
try:
    import cv2
except ImportError:
    print("⚠️ OpenCV non installé. Utilisation de PIL uniquement pour les visualisations.")
    
    def create_overlay_visualization(original_img, colored_mask, output_dir):
        """Version PIL uniquement de la superposition"""
        # Convertir en mode RGBA
        original_rgba = original_img.convert("RGBA")
        
        # Créer le masque avec transparence
        mask_img = Image.fromarray(colored_mask)
        mask_rgba = mask_img.convert("RGBA")
        
        # Ajuster la transparence
        mask_data = mask_rgba.getdata()
        new_data = []
        for item in mask_data:
            # Réduire l'opacité à 50%
            new_data.append((item[0], item[1], item[2], 128))
        mask_rgba.putdata(new_data)
        
        # Superposer
        overlay = Image.alpha_composite(original_rgba, mask_rgba)
        
        # Sauvegarder
        overlay_path = os.path.join(output_dir, "visualization_overlay.png")
        overlay.convert("RGB").save(overlay_path)
        print(f"✅ Visualisation avec superposition sauvegardée: visualization_overlay.png")

if __name__ == "__main__":
    # Vérifier qu'on est dans le bon dossier
    current_dir = os.getcwd()
    print(f"📁 Dossier actuel: {current_dir}")
    
    if not current_dir.endswith('test-prediction'):
        print("⚠️  Attention: Il est recommandé d'exécuter ce script depuis le dossier test-prediction/")
    
    # Lancer les tests
    test_api()
    
    # Visualiser les résultats
    print("\n" + "="*70)
    visualize_results()