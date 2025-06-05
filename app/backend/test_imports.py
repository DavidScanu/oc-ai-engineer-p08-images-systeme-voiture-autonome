# app/fastapi/test_imports.py
print("🔍 Test des imports...")

try:
    import tensorflow as tf
    print(f"✅ TensorFlow {tf.__version__}")
except ImportError as e:
    print(f"❌ TensorFlow: {e}")

try:
    import keras
    print(f"✅ Keras {keras.__version__}")
except ImportError as e:
    print(f"❌ Keras: {e}")

try:
    import numpy as np
    print(f"✅ NumPy {np.__version__}")
except ImportError as e:
    print(f"❌ NumPy: {e}")

try:
    import mlflow
    print(f"✅ MLflow {mlflow.__version__}")
except ImportError as e:
    print(f"❌ MLflow: {e}")

try:
    import fastapi
    print(f"✅ FastAPI {fastapi.__version__}")
except ImportError as e:
    print(f"❌ FastAPI: {e}")

print("\n✨ Test terminé!")