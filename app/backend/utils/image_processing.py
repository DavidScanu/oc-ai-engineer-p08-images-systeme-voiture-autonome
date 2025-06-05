# app/fastapi/utils/image_processing.py
import numpy as np
from PIL import Image
import io
import base64
from typing import Tuple

def decode_base64_image(base64_string: str) -> Image.Image:
    """Décode une image base64 en objet PIL Image"""
    # Enlever le préfixe data:image/...;base64, si présent
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    
    # Décoder le base64
    img_bytes = base64.b64decode(base64_string)
    
    # Créer l'objet PIL Image
    img = Image.open(io.BytesIO(img_bytes))
    
    return img

def encode_image_to_base64(image: Image.Image) -> str:
    """Encode une image PIL en base64"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def numpy_to_pil(numpy_array: np.ndarray) -> Image.Image:
    """Convertit un array numpy en image PIL"""
    return Image.fromarray(numpy_array.astype('uint8'))

def validate_image(image: Image.Image, max_size: Tuple[int, int] = (4096, 4096)) -> bool:
    """Valide que l'image est dans les limites acceptables"""
    width, height = image.size
    return width <= max_size[0] and height <= max_size[1]