from ai.predictor import MODEL

base_model = MODEL.get_layer("efficientnetb0")

for layer in base_model.layers[-20:]:
    print(layer.name)