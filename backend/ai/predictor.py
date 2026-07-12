import tensorflow as tf

from ai.preprocessing import preprocess_image
from ai.labels import CLASS_NAMES

MODEL = tf.keras.models.load_model(
    "ai/models/chest_xray_model.keras"
)


def predict(image_path):

    image = preprocess_image(image_path)

    prediction = MODEL.predict(image)

    predicted_index = prediction.argmax()

    confidence = float(prediction.max())

    return {

        "disease": CLASS_NAMES[predicted_index],

        "confidence": round(confidence * 100, 2)

    }