import json
import shutil
import numpy as np
import pandas as pd
import tensorflow as tf

from pathlib import Path
from tensorflow.keras.models import load_model

# ==========================================
# 1. CONFIGURATION
# ==========================================
BASE_DIR = Path(__file__).resolve().parents[3]

TEST_DIR = (
    BASE_DIR
    / "datasets"
    / "archive"
    / "dataset_split"
    / "test"
)

MODEL_DIR = (
    BASE_DIR
    / "models"
    / "archive"
    / "24_breed_models"
    / "models2"
)

MODEL_PATH = MODEL_DIR / "mobilenetv2_24breed_finetuned_best.keras"

OUTPUT_DIR = (
    BASE_DIR
    / "results"
    / "error_analysis"
    / "24_breed"
    / "misclassified_images"
)

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16

# ==========================================
# 2. LOAD CLASS NAMES
# ==========================================

with open(MODEL_DIR / "class_names.json", "r") as f:
    class_names = json.load(f)

print("Total breeds:", len(class_names))

# ==========================================
# 3. LOAD TEST DATASET
# ==========================================

test_dataset = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=False
)

if test_dataset.class_names != class_names:
    raise ValueError("Class names do not match!")

image_paths = test_dataset.file_paths

y_true = np.concatenate([
    labels.numpy()
    for _, labels in test_dataset
])

print("Total test images:", len(image_paths))

# ==========================================
# 4. LOAD MODEL
# ==========================================

print("\nLoading fine-tuned model...")

model = load_model(MODEL_PATH)

# ==========================================
# 5. MAKE PREDICTIONS
# ==========================================

print("\nPredicting test images...")

predictions = model.predict(test_dataset, verbose=1)

y_pred = np.argmax(predictions, axis=1)

confidence_scores = np.max(predictions, axis=1)

# ==========================================
# 6. IDENTIFY MISCLASSIFIED IMAGES
# ==========================================

records = []

correct_count = 0
incorrect_count = 0

for i in range(len(y_true)):

    actual_index = int(y_true[i])
    predicted_index = int(y_pred[i])

    actual_breed = class_names[actual_index]
    predicted_breed = class_names[predicted_index]

    confidence = float(confidence_scores[i])

    if actual_index == predicted_index:
        correct_count += 1
        continue

    incorrect_count += 1

    source_path = Path(image_paths[i])

    # Create folder for actual breed
    breed_folder = OUTPUT_DIR / actual_breed
    breed_folder.mkdir(parents=True, exist_ok=True)

    # Copy image
    destination = breed_folder / source_path.name
    shutil.copy2(source_path, destination)

    records.append({
        "image_name": source_path.name,
        "actual_breed": actual_breed,
        "predicted_breed": predicted_breed,
        "confidence": round(confidence * 100, 2),
        "image_path": str(source_path)
    })

# ==========================================
# 7. SAVE CSV
# ==========================================

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.DataFrame(records)

csv_path = OUTPUT_DIR / "misclassified_predictions.csv"

df.to_csv(csv_path, index=False)

# ==========================================
# 8. PRINT SUMMARY
# ==========================================

print("\n========== MISCLASSIFICATION SUMMARY ==========")

print("Total test images:", len(y_true))
print("Correct predictions:", correct_count)
print("Incorrect predictions:", incorrect_count)

accuracy = correct_count / len(y_true) * 100

print(f"Test accuracy: {accuracy:.2f}%")

print("\nMISCLASSIFIED IMAGES BY BREED")

if not df.empty:
    breed_counts = (
        df.groupby("actual_breed")
        .size()
        .sort_values(ascending=False)
    )

    print(breed_counts.to_string())
else:
    print("No misclassified images found.")

print("\nCSV saved at:", csv_path)
print("Images saved at:", OUTPUT_DIR)

print("\nAnalysis completed!")