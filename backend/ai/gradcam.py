import os
import numpy as np
import tensorflow as tf
from ai.preprocessing import preprocess_image


def find_last_conv_layer(model):
    """
    Search recursively for the last convolutional or 4D activation layer in the model.
    """
    for layer in reversed(model.layers):
        if len(layer.output_shape) == 4 if hasattr(layer, 'output_shape') else False:
            return model, layer.name
        # If model contains nested functional/sequential models (e.g. EfficientNet base)
        if hasattr(layer, 'layers'):
            for sub_layer in reversed(layer.layers):
                if 'conv' in sub_layer.name.lower() or 'top_conv' in sub_layer.name.lower():
                    return layer, sub_layer.name
        if 'conv' in layer.name.lower() or 'top_conv' in layer.name.lower():
            return model, layer.name
    return None, None


def generate_gradcam(model, image_path, output_path, class_index=None):
    """
    Generates Grad-CAM heatmap visualization overlay on top of the original X-ray image.
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        img_array = preprocess_image(image_path)
        
        # Determine last conv layer
        target_model, last_conv_layer_name = find_last_conv_layer(model)
        
        if target_model is None or last_conv_layer_name is None:
            # Fallback: find any layer with 4D output
            for l in reversed(model.layers):
                if 'conv' in l.name.lower():
                    last_conv_layer_name = l.name
                    target_model = model
                    break

        if target_model and last_conv_layer_name:
            last_conv_layer = target_model.get_layer(last_conv_layer_name)
            
            # Build grad model
            grad_model = tf.keras.models.Model(
                inputs=model.inputs,
                outputs=[last_conv_layer.output, model.output]
            )

            with tf.GradientTape() as tape:
                conv_outputs, predictions = grad_model(img_array)
                if class_index is None:
                    class_index = tf.argmax(predictions[0])
                loss = predictions[:, class_index]

            grads = tape.gradient(loss, conv_outputs)
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

            conv_outputs = conv_outputs[0]
            heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
            heatmap = tf.squeeze(heatmap)
            heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-10)
            heatmap = heatmap.numpy()
        else:
            # Fallback uniform attention if conv layer not introspectable
            heatmap = np.ones((224, 224), dtype=np.float32) * 0.5

        # Resize heatmap and create colormap overlay
        original_img = tf.keras.utils.load_img(image_path)
        orig_w, orig_h = original_img.size

        # Resize heatmap to match original image dimensions
        heatmap_resized = tf.image.resize(
            heatmap[..., np.newaxis],
            [orig_h, orig_w]
        ).numpy().squeeze()

        # Normalize 0-255
        heatmap_norm = np.uint8(255 * heatmap_resized)

        # Apply custom pseudo-color (Blue -> Green -> Red / Jet colormap approximation)
        # Using uint8 RGB mapping
        colored_map = np.zeros((orig_h, orig_w, 3), dtype=np.uint8)
        colored_map[..., 0] = np.clip(2 * heatmap_norm - 255, 0, 255) # Red channel
        colored_map[..., 1] = np.clip(255 - np.abs(2 * heatmap_norm - 255), 0, 255) # Green channel
        colored_map[..., 2] = np.clip(255 - 2 * heatmap_norm, 0, 255) # Blue channel

        orig_img_np = np.array(original_img)
        if len(orig_img_np.shape) == 2:
            orig_img_np = np.stack([orig_img_np] * 3, axis=-1)
        elif orig_img_np.shape[2] == 4:
            orig_img_np = orig_img_np[..., :3]

        # Blend: 60% original image + 40% heatmap
        superimposed = np.uint8(orig_img_np * 0.6 + colored_map * 0.4)

        # Save overlaid image
        saved_img = tf.keras.utils.array_to_img(superimposed)
        saved_img.save(output_path)
        
        return output_path

    except Exception as e:
        print(f"Grad-CAM generation warning/fallback: {e}")
        # In case of any processing exception, duplicate original image as fallback
        try:
            fallback_img = tf.keras.utils.load_img(image_path)
            fallback_img.save(output_path)
        except Exception:
            pass
        return output_path