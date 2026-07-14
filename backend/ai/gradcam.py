import os

import cv2
import numpy as np
import tensorflow as tf

from ai.preprocessing import preprocess_image


LAST_CONV_LAYER = "top_conv"


def generate_gradcam(
    model,
    image_path,
    output_path
):

    img = preprocess_image(image_path)

    grad_model = tf.keras.models.Model(

        model.inputs,

        [
            model.get_layer(LAST_CONV_LAYER).output,
            model.output
        ]

    )

    with tf.GradientTape() as tape:

        conv_outputs, predictions = grad_model(img)

        predicted_class = tf.argmax(predictions[0])

        loss = predictions[:, predicted_class]

    gradients = tape.gradient(loss, conv_outputs)

    pooled_gradients = tf.reduce_mean(

        gradients,

        axis=(0, 1, 2)

    )

    conv_outputs = conv_outputs[0]

    heatmap = conv_outputs @ pooled_gradients[..., tf.newaxis]

    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(

        heatmap,

        0

    ) / tf.math.reduce_max(heatmap)

    heatmap = heatmap.numpy()

    original = cv2.imread(image_path)

    heatmap = cv2.resize(

        heatmap,

        (

            original.shape[1],

            original.shape[0]

        )

    )

    heatmap = np.uint8(255 * heatmap)

    heatmap = cv2.applyColorMap(

        heatmap,

        cv2.COLORMAP_JET

    )

    superimposed = cv2.addWeighted(

        original,

        0.6,

        heatmap,

        0.4,

        0

    )

    os.makedirs(

        os.path.dirname(output_path),

        exist_ok=True

    )

    cv2.imwrite(

        output_path,

        superimposed

    )

    return output_path