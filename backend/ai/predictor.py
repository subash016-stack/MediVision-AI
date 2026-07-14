from ai.model_loader import get_model
from ai.preprocessing import preprocess_image
from ai.labels import CLASS_NAMES


def predict(image_path):

    model = get_model()

    image = preprocess_image(image_path)

    prediction = model.predict(
        image,
        verbose=0
    )

    index = prediction.argmax()

    confidence = float(prediction.max())

    return {

        "disease": CLASS_NAMES[index],

        "confidence": round(confidence * 100, 2)

    }