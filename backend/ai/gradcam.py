import os


def generate_gradcam(model, image_path, output_path):

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    # Placeholder
    # Real Grad-CAM implementation will be added later.

    return output_path