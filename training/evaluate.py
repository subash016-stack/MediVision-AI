import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from data_loader import load_datasets

DATASET_PATH = "dataset"

_, _, test_ds, class_names = load_datasets(DATASET_PATH)

model = tf.keras.models.load_model(
    "models/best_model.keras"
)

loss, accuracy = model.evaluate(test_ds)

print("\n==========================")
print(f"Test Accuracy : {accuracy*100:.2f}%")
print(f"Test Loss     : {loss:.4f}")
print("==========================\n")

y_true = []
y_pred = []

for images, labels in test_ds:

    predictions = model.predict(images, verbose=0)

    predicted = np.argmax(predictions, axis=1)

    y_true.extend(labels.numpy())

    y_pred.extend(predicted)

report = classification_report(
    y_true,
    y_pred,
    target_names=class_names
)

print(report)

os.makedirs("results", exist_ok=True)

with open(
    "results/classification_report.txt",
    "w"
) as f:

    f.write(report)

cm = confusion_matrix(y_true, y_pred)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=class_names
)

fig, ax = plt.subplots(figsize=(8, 8))

disp.plot(ax=ax)

plt.savefig(
    "results/confusion_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nEvaluation Completed Successfully!")