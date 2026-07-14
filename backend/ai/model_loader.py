import tensorflow as tf

MODEL = tf.keras.models.load_model(
    "ai/models/chest_xray_model.keras"
)

BASE_MODEL = MODEL.get_layer("efficientnetb0")