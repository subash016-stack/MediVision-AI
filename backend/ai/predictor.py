import random

DISEASES = [
    "Normal",
    "Pneumonia",
    "COVID-19",
    "Tuberculosis"
]


def predict(image_path):

    return {
        "disease": random.choice(DISEASES),
        "confidence": round(random.uniform(90, 99), 2)
    }