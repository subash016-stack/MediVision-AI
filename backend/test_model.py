# test_model.py

from ai.model_loader import MODEL, BASE_MODEL

print("Main Model")
MODEL.summary()

print("\n\nBase Model")
BASE_MODEL.summary()

print("\nLast Layers")

for layer in BASE_MODEL.layers[-15:]:
    print(layer.name, layer.output.shape)