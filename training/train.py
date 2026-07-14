from datetime import datetime

from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau,
    TensorBoard
)

from data_loader import load_datasets
from model import build_model

DATASET_PATH = "dataset"

train_ds, valid_ds, test_ds, class_names = load_datasets(DATASET_PATH)

print("\nClasses:")
print(class_names)

model = build_model()

callbacks = [

    EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    ),

    ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.2,
        patience=3,
        verbose=1
    ),

    ModelCheckpoint(
        filepath="models/best_model.keras",
        monitor="val_accuracy",
        save_best_only=True,
        verbose=1
    ),

    TensorBoard(
        log_dir=f"logs/{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    )

]

history = model.fit(

    train_ds,

    validation_data=valid_ds,

    epochs=20,

    callbacks=callbacks

)

model.save("models/final_model.keras")

print("\nTraining Completed Successfully!")