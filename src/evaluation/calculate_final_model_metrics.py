import json
import numpy as np
import tensorflow as tf

from pathlib import Path
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)


# ============================================================
# 1. CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

TEST_DIR = (
    BASE_DIR / "datasets" / "active"
    / "dataset_18breeds_split_jpeg" / "test"
)

MODEL_PATH = (
    BASE_DIR / "models" / "final"
    / "mobilenetv2_18breed_finetuned_best.keras"
)

CLASS_NAMES_PATH = (
    BASE_DIR / "models" / "final"
    / "class_names_18breed.json"
)

RESULT_DIR = (
    BASE_DIR / "results" / "evaluation"
    / "final_model_metrics"
)

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
EXPECTED_CLASSES = 18


# ============================================================
# 2. CHECK REQUIRED FILES
# ============================================================

required_paths = [
    TEST_DIR,
    MODEL_PATH,
    CLASS_NAMES_PATH
]

for path in required_paths:
    if not path.exists():
        raise FileNotFoundError(f"Required path not found: {path}")


# ============================================================
# 3. LOAD CLASS NAMES
# ============================================================

with open(CLASS_NAMES_PATH, "r") as file:
    class_names = json.load(file)

if len(class_names) != EXPECTED_CLASSES:
    raise ValueError("Expected exactly 18 cattle breeds.")


# ============================================================
# 4. LOAD TEST DATASET
# ============================================================

print("\nLoading test dataset...")

test_dataset = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=False
)

if test_dataset.class_names != class_names:
    raise ValueError("Test dataset class order mismatch!")


# ============================================================
# 5. LOAD FINAL MODEL
# ============================================================

print("\nLoading final MobileNetV2 model...")

model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

if model.output_shape[-1] != EXPECTED_CLASSES:
    raise ValueError("Model output does not match 18 classes.")

print("Final model loaded successfully.")


# ============================================================
# 6. GET ACTUAL LABELS
# ============================================================

y_true = np.concatenate([
    labels.numpy()
    for _, labels in test_dataset
])


# ============================================================
# 7. PREDICT TEST IMAGES
# ============================================================

print("\nPredicting test images...")

predictions = model.predict(
    test_dataset,
    verbose=1
)

y_pred = np.argmax(predictions, axis=1)


# ============================================================
# 8. OVERALL EVALUATION METRICS
# ============================================================

accuracy = accuracy_score(y_true, y_pred)

macro_precision = precision_score(
    y_true, y_pred,
    average="macro",
    zero_division=0
)

macro_recall = recall_score(
    y_true, y_pred,
    average="macro",
    zero_division=0
)

macro_f1 = f1_score(
    y_true, y_pred,
    average="macro",
    zero_division=0
)

weighted_precision = precision_score(
    y_true, y_pred,
    average="weighted",
    zero_division=0
)

weighted_recall = recall_score(
    y_true, y_pred,
    average="weighted",
    zero_division=0
)

weighted_f1 = f1_score(
    y_true, y_pred,
    average="weighted",
    zero_division=0
)


# ============================================================
# 9. BREED-WISE METRICS
# ============================================================

report = classification_report(
    y_true,
    y_pred,
    labels=list(range(EXPECTED_CLASSES)),
    target_names=class_names,
    output_dict=True,
    zero_division=0
)


# ============================================================
# 10. DISPLAY OVERALL RESULTS
# ============================================================

print("\n" + "=" * 75)
print("             CATTLE VISION - FINAL MODEL EVALUATION")
print("=" * 75)

print(f"Total Test Images : {len(y_true)}")
print(f"Correct Predictions: {np.sum(y_true == y_pred)}")
print(f"Wrong Predictions  : {np.sum(y_true != y_pred)}")

print("\nOVERALL PERFORMANCE")
print("-" * 75)

print(f"Accuracy           : {accuracy * 100:.2f}%")
print(f"Macro Precision    : {macro_precision * 100:.2f}%")
print(f"Macro Recall       : {macro_recall * 100:.2f}%")
print(f"Macro F1-score     : {macro_f1 * 100:.2f}%")

print(f"Weighted Precision : {weighted_precision * 100:.2f}%")
print(f"Weighted Recall    : {weighted_recall * 100:.2f}%")
print(f"Weighted F1-score  : {weighted_f1 * 100:.2f}%")


# ============================================================
# 11. DISPLAY BREED-WISE RESULTS
# ============================================================

print("\nBREED-WISE PERFORMANCE")
print("-" * 95)

print(
    f"{'Breed':<22}"
    f"{'Precision':>12}"
    f"{'Recall':>12}"
    f"{'F1-score':>12}"
    f"{'Support':>12}"
)

print("-" * 95)

breed_results = {}

for breed in class_names:

    breed_metrics = report[breed]

    precision = breed_metrics["precision"]
    recall = breed_metrics["recall"]
    f1 = breed_metrics["f1-score"]
    support = int(breed_metrics["support"])

    print(
        f"{breed:<22}"
        f"{precision * 100:>11.2f}%"
        f"{recall * 100:>11.2f}%"
        f"{f1 * 100:>11.2f}%"
        f"{support:>12}"
    )

    breed_results[breed] = {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "support": support
    }


# ============================================================
# 12. SAVE RESULTS
# ============================================================

RESULT_DIR.mkdir(parents=True, exist_ok=True)

results = {
    "model": MODEL_PATH.name,
    "total_test_images": int(len(y_true)),
    "correct_predictions": int(np.sum(y_true == y_pred)),
    "wrong_predictions": int(np.sum(y_true != y_pred)),

    "overall_metrics": {
        "accuracy": float(accuracy),
        "macro_precision": float(macro_precision),
        "macro_recall": float(macro_recall),
        "macro_f1_score": float(macro_f1),
        "weighted_precision": float(weighted_precision),
        "weighted_recall": float(weighted_recall),
        "weighted_f1_score": float(weighted_f1)
    },

    "breed_wise_metrics": breed_results
}

output_path = RESULT_DIR / "final_model_metrics.json"

if output_path.exists():
    raise FileExistsError(
        f"Results already exist: {output_path}. "
        "Rename or back up the existing file before running again."
    )

with open(output_path, "w") as file:
    json.dump(results, file, indent=4)


# ============================================================
# 13. COMPLETION
# ============================================================

print("\n" + "=" * 75)
print("FINAL MODEL EVALUATION COMPLETED")
print("=" * 75)

print("\nResults saved at:")
print(output_path)