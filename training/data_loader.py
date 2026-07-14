import tensorflow as tf

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
AUTOTUNE = tf.data.AUTOTUNE


def load_datasets(dataset_path):

    train_dataset = tf.keras.utils.image_dataset_from_directory(
        f"{dataset_path}/train",
        validation_split=0.15,
        subset="training",
        seed=42,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="int"
    )

    validation_dataset = tf.keras.utils.image_dataset_from_directory(
        f"{dataset_path}/train",
        validation_split=0.15,
        subset="validation",
        seed=42,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="int"
    )

    test_dataset = tf.keras.utils.image_dataset_from_directory(
        f"{dataset_path}/test",
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False,
        label_mode="int"
    )

    class_names = train_dataset.class_names

    train_dataset = train_dataset.prefetch(AUTOTUNE)
    validation_dataset = validation_dataset.prefetch(AUTOTUNE)
    test_dataset = test_dataset.prefetch(AUTOTUNE)

    return train_dataset, validation_dataset, test_dataset, class_names