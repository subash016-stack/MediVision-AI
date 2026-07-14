import tensorflow as tf

MODEL_PATH = "ai/models/chest_xray_model.keras"

_model = None


def get_model():
    global _model

    if _model is None:
        print("Loading AI model...")
        _model = tf.keras.models.load_model(MODEL_PATH)
        print("Model loaded successfully!")

    return _model