from ai.preprocessing import preprocess_image
from ai.labels import CLASS_NAMES
from ai.model_loader import MODEL


def predict(image_path):

    image = preprocess_image(image_path)

    prediction = MODEL.predict(
        image,
        verbose=0
    )

    predicted_index = prediction.argmax()

    confidence = float(prediction.max())

    return {

        "disease": CLASS_NAMES[predicted_index],

        "confidence": round(confidence * 100, 2)

    }