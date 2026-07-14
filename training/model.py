import tensorflow as tf

from augmentation import data_augmentation


def build_model():

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

    x = tf.keras.layers.Dropout(0.3)(x)

    outputs = tf.keras.layers.Dense(
        4,
        activation="softmax"
    )(x)

    model = tf.keras.Model(inputs, outputs)

    model.compile(

        optimizer=tf.keras.optimizers.Adam(0.001),

        loss="sparse_categorical_crossentropy",

        metrics=[
            "accuracy"
        ]

    )

    return model