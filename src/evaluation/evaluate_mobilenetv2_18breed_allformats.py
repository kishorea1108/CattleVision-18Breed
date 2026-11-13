import os
import json
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)

# ============================================================
# 1. CONFIGURATION
# ============================================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

TEST_DIR = BASE_DIR / "datasets" / "active" / "dataset_18breeds_split_jpeg" / "test"

MODEL_PATH = BASE_DIR / "models" / "experiments" / "all_formats" / "mobilenetv2_18breed_allformats_best.keras"

CLASS_NAMES_PATH = BASE_DIR / "models" / "experiments" / "all_formats" / "class_names_18breed_allformats.json"

RESULT_DIR = BASE_DIR / "results" / "evaluation" / "all_formats_initial"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
EXPECTED_TEST_IMAGES = 558

# Prevent accidental overwriting of existing evaluation results
OUTPUT_FILES = [
    RESULT_DIR / "classification_report.txt",
    RESULT_DIR / "confusion_matrix.png",
    RESULT_DIR / "evaluation_metrics.json"
]

existing_files = [path for path in OUTPUT_FILES if path.exists()]

if existing_files:
    raise FileExistsError(
        "Evaluation results already exist. "
        "Choose a new result directory or filenames:\n"
        + "\n".join(str(path) for path in existing_files)
    )

RESULT_DIR.mkdir(parents=True, exist_ok=True)
# ============================================================
# 2. LOAD CLASS NAMES
# ============================================================

with open(CLASS_NAMES_PATH, "r") as file:
    class_names = json.load(file)

NUM_CLASSES = len(class_names)

if NUM_CLASSES != 18:
    raise ValueError("Expected exactly 18 classes.")

# ============================================================
# 3. LOAD TEST DATASET
# ============================================================

test_dataset = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=False
)

if test_dataset.class_names != class_names:
    raise ValueError("Test class order mismatch.")

# Count actual loaded images
actual_test_count = sum(
    len(labels)
    for _, labels in test_dataset
)

print("Images loaded by TensorFlow:", actual_test_count)

if actual_test_count != EXPECTED_TEST_IMAGES:
    raise ValueError(
        f"Expected {EXPECTED_TEST_IMAGES} images, "
        f"but TensorFlow loaded {actual_test_count}."
    )

test_dataset = test_dataset.prefetch(tf.data.AUTOTUNE)

# ============================================================
# 4. LOAD FINE-TUNED MODEL
# ============================================================

model = tf.keras.models.load_model(MODEL_PATH)

print("\nFine-tuned model loaded successfully.")

# ============================================================
# 5. GET ACTUAL LABELS
# ============================================================

y_true = np.concatenate([
    labels.numpy()
    for _, labels in test_dataset
])

# ============================================================
# 6. PREDICTIONS
# ============================================================

print("\nPredicting all test images...")

predictions = model.predict(test_dataset)

y_pred = np.argmax(predictions, axis=1)

if len(y_true) != EXPECTED_TEST_IMAGES:
    raise ValueError("Incorrect number of actual labels.")

if len(y_pred) != EXPECTED_TEST_IMAGES:
    raise ValueError("Incorrect number of predictions.")

# ============================================================
# 7. EVALUATION METRICS
# ============================================================

accuracy = accuracy_score(y_true, y_pred)

precision = precision_score(
    y_true,
    y_pred,
    average="macro",
    zero_division=0
)

recall = recall_score(
    y_true,
    y_pred,
    average="macro",
    zero_division=0
)

f1 = f1_score(
    y_true,
    y_pred,
    average="macro",
    zero_division=0
)

weighted_f1 = f1_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

print("\n" + "=" * 65)
print("FINAL TEST RESULTS - 18 BREEDS")
print("=" * 65)

print("Total test images:", len(y_true))

print(f"Accuracy       : {accuracy * 100:.2f}%")
print(f"Macro Precision: {precision * 100:.2f}%")
print(f"Macro Recall   : {recall * 100:.2f}%")
print(f"Macro F1-score : {f1 * 100:.2f}%")
print(f"Weighted F1    : {weighted_f1 * 100:.2f}%")

# ============================================================
# 8. CLASSIFICATION REPORT
# ============================================================

report = classification_report(
    y_true,
    y_pred,
    target_names=class_names,
    zero_division=0
)

print("\nCLASSIFICATION REPORT")
print("=" * 65)
print(report)

with open(
    os.path.join(RESULT_DIR, "classification_report.txt"),
    "w"
) as file:
    file.write(report)

# ============================================================
# 9. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_true,
    y_pred,
    labels=list(range(NUM_CLASSES))
)

plt.figure(figsize=(16, 13))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=class_names,
    yticklabels=class_names
)

plt.title("CattleVision - 18 Breed Final Confusion Matrix")
plt.xlabel("Predicted Breed")
plt.ylabel("Actual Breed")

plt.xticks(rotation=90)
plt.yticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(RESULT_DIR, "confusion_matrix.png"),
    dpi=300
)

plt.show()

# ============================================================
# 10. SAVE METRICS
# ============================================================

results = {
    "total_test_images": int(len(y_true)),
    "accuracy": float(accuracy),
    "macro_precision": float(precision),
    "macro_recall": float(recall),
    "macro_f1_score": float(f1),
    "weighted_f1_score": float(weighted_f1)
}

with open(
    os.path.join(RESULT_DIR, "evaluation_metrics.json"),
    "w"
) as file:
    json.dump(results, file, indent=4)

# ============================================================
# 11. COMPLETION
# ============================================================

print("\nEvaluation files saved in:", RESULT_DIR)

print("\n" + "=" * 65)
print("FINAL EVALUATION COMPLETED SUCCESSFULLY")
print("=" * 65)