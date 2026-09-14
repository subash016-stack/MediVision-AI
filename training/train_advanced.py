import os
import numpy as np
import tensorflow as tf
from datetime import datetime
import shutil

from data_loader import load_datasets
from augmentation import data_augmentation

DATASET_PATH = "dataset"


def compute_class_weights(dataset_path, class_names):
    """
    Computes balanced class weights to address dataset class imbalance.
    """
    train_dir = os.path.join(dataset_path, "train")
    counts = []
    for cls in class_names:
        cls_dir = os.path.join(train_dir, cls)
        counts.append(len(os.listdir(cls_dir)))
    
    total = sum(counts)
    n_classes = len(class_names)
    weights = {i: total / (n_classes * count) for i, count in enumerate(counts)}
    print("\n--- Computed Class Weights ---")
    for i, cls in enumerate(class_names):
        print(f"  Class {i} ({cls:15}): {weights[i]:.3f} (Count: {counts[i]})")
    return weights


def build_transfer_model(num_classes=4):
    """
    Builds EfficientNetB0 transfer learning architecture.
    """
    base_model = tf.keras.applications.EfficientNetB0(
        weights="imagenet",
        include_top=False,
        input_shape=(224, 224, 3)
    )
    base_model.trainable = False

    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = data_augmentation(inputs)
    x = tf.keras.applications.efficientnet.preprocess_input(x)
    x = base_model(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.35)(x)
    x = tf.keras.layers.Dense(128, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.25)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)

    model = tf.keras.Model(inputs, outputs)
    return model, base_model


def main():
    print("==================================================")
    print("MediVision-AI Advanced Training & Fine-Tuning Pipeline")
    print("==================================================\n")

    os.makedirs("models", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    train_ds, valid_ds, test_ds, class_names = load_datasets(DATASET_PATH)
    class_weights = compute_class_weights(DATASET_PATH, class_names)

    model, base_model = build_transfer_model(len(class_names))

    # -------------------------------------------------------------
    # STAGE 1: Train Top Classifier Head (Feature Extraction)
    # -------------------------------------------------------------
    print("\n>>> STAGE 1: Training Classification Head (Base Frozen) <<<")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    callbacks_stage1 = [
        tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=3, restore_best_weights=True)
    ]

    model.fit(
        train_ds,
        validation_data=valid_ds,
        epochs=5,
        class_weight=class_weights,
        callbacks=callbacks_stage1,
        verbose=1
    )

    # -------------------------------------------------------------
    # STAGE 2: Fine-Tuning (Unfreezing Top 35 Layers of EfficientNet)
    # -------------------------------------------------------------
    print("\n>>> STAGE 2: Fine-Tuning Top 35 Layers of EfficientNetB0 <<<")
    base_model.trainable = True
    for layer in base_model.layers[:-35]:
        layer.trainable = False

    fine_tune_lr = 1e-5
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=fine_tune_lr),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    checkpoint_path = "models/best_model.keras"
    callbacks_stage2 = [
        tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_path,
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.2,
            patience=2,
            min_lr=1e-7,
            verbose=1
        )
    ]

    model.fit(
        train_ds,
        validation_data=valid_ds,
        epochs=15,
        class_weight=class_weights,
        callbacks=callbacks_stage2,
        verbose=1
    )

    # -------------------------------------------------------------
    # STAGE 3: Final Test Evaluation & Deployment Sync
    # -------------------------------------------------------------
    print("\n>>> STAGE 3: Test Dataset Evaluation <<<")
    best_model = tf.keras.models.load_model(checkpoint_path)
    test_loss, test_acc = best_model.evaluate(test_ds)
    print(f"\nFinal Test Accuracy: {test_acc * 100:.2f}% | Test Loss: {test_loss:.4f}")

    # Copy best model to backend and trained_models
    backend_model_dest = os.path.join("..", "backend", "ai", "models", "chest_xray_model.keras")
    trained_model_dest = os.path.join("..", "trained_models", "chest_xray_model.keras")
    
    os.makedirs(os.path.dirname(backend_model_dest), exist_ok=True)
    os.makedirs(os.path.dirname(trained_model_dest), exist_ok=True)
    
    shutil.copyfile(checkpoint_path, backend_model_dest)
    shutil.copyfile(checkpoint_path, trained_model_dest)
    print(f"\n[OK] Upgraded model synced to backend: {backend_model_dest}")


if __name__ == "__main__":
    main()
