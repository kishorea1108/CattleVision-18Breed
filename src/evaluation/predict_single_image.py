
import json
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from pathlib import Path
from PIL import Image


# ============================================================
# 1. CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    BASE_DIR / "models" / "final"
    / "mobilenetv2_18breed_finetuned_best.keras"
)

CLASS_NAMES_PATH = (
    BASE_DIR / "models" / "final"
    / "class_names_18breed.json"
)

IMAGE_SIZE = (224, 224)


# ============================================================
# 2. LOAD MODEL AND CLASS NAMES
# ============================================================

def load_model():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    if not CLASS_NAMES_PATH.exists():
        raise FileNotFoundError(
            f"Class names not found: {CLASS_NAMES_PATH}"
        )

    with open(CLASS_NAMES_PATH, "r") as file:
        class_names = json.load(file)

    if len(class_names) != 18:
        raise ValueError("Expected exactly 18 cattle breeds.")

    print("\nLoading CattleVision final model...")

    model = tf.keras.models.load_model(
        MODEL_PATH,
        compile=False
    )

    if model.output_shape[-1] != len(class_names):
        raise ValueError("Model output and class count mismatch.")

    print("Model loaded successfully.")

    return model, class_names


# ============================================================
# 3. IMAGE PREPROCESSING
# ============================================================

def preprocess_image(image_path):

    image = Image.open(image_path).convert("RGB")

    image = image.resize(IMAGE_SIZE)

    image_array = np.array(image, dtype=np.float32)

    image_array = np.expand_dims(image_array, axis=0)

    return image, image_array


# ============================================================
# 4. PREDICTION
# ============================================================

def predict_breed(model, class_names, image_path):

    image, image_array = preprocess_image(image_path)

    predictions = model.predict(
        image_array,
        verbose=0
    )[0]

    predicted_index = int(np.argmax(predictions))

    predicted_breed = class_names[predicted_index]

    confidence = float(predictions[predicted_index]) * 100

    top_indices = np.argsort(predictions)[-3:][::-1]

    # Display results

    print("\n" + "=" * 60)
    print("          CATTLE VISION - PREDICTION RESULTS")
    print("=" * 60)

    print(f"\nPredicted Breed : {predicted_breed}")
    print(f"Confidence      : {confidence:.2f}%")

    print("\nTOP 3 PREDICTIONS")
    print("-" * 45)

    for rank, index in enumerate(top_indices, start=1):

        breed = class_names[index]

        score = float(predictions[index]) * 100

        print(f"{rank}. {breed:<22} {score:.2f}%")

    print("=" * 60)

    # Display image

    plt.figure(figsize=(8, 7))

    plt.imshow(image)

    plt.title(
        f"Predicted Breed: {predicted_breed}\n"
        f"Confidence: {confidence:.2f}%",
        fontsize=13
    )

    plt.axis("off")

    plt.tight_layout()

    plt.show()


# ============================================================
# 5. MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    try:

        model, class_names = load_model()

        while True:

            print("\nEnter cattle image path.")

            image_path = input("Image Path: ").strip().strip('"')

            if not image_path:
                print("Please enter a valid image path.")
                continue

            image_path = Path(image_path).expanduser()

            if not image_path.is_file():
                print("\nError: Image file not found.")
                continue

            try:

                predict_breed(
                    model,
                    class_names,
                    image_path
                )

            except Exception as error:

                print(f"\nPrediction failed: {error}")

            choice = input(
                "\nDo you want to predict another image? (y/n): "
            ).strip().lower()

            if choice != "y":
                print("\nCattleVision prediction session ended.")
                break

    except Exception as error:

        print(f"\nApplication error: {error}")
