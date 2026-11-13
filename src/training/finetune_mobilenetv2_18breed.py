import os
import json
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.callbacks import (
    ModelCheckpoint,
    EarlyStopping,
    ReduceLROnPlateau
)

# ============================================================
# 1. CONFIGURATION
# ============================================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

TRAIN_DIR = BASE_DIR / "datasets" / "archive" / "dataset_18breeds_split" / "train"
VAL_DIR = BASE_DIR / "datasets" / "archive" / "dataset_18breeds_split" / "validation"

INITIAL_MODEL_PATH = BASE_DIR / "models" / "experiments" / "original_format" / "mobilenetv2_18breed_best.keras"

FINETUNED_MODEL_PATH = BASE_DIR / "models" / "experiments" / "original_format" / "mobilenetv2_18breed_finetuned_best.keras"

CLASS_NAMES_PATH = BASE_DIR / "models" / "final" / "class_names_18breed.json"

HISTORY_PATH = BASE_DIR / "models" / "experiments" / "original_format" / "finetuning_history_18breed.json"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 10
NUM_CLASSES = 18
LEARNING_RATE = 0.00001
UNFREEZE_LAST_LAYERS = 30
SEED = 42
# Prevent accidental overwriting of existing fine-tuning outputs
OUTPUT_FILES = [
    FINETUNED_MODEL_PATH,
    HISTORY_PATH
]

existing_files = [path for path in OUTPUT_FILES if path.exists()]

if existing_files:
    raise FileExistsError(
        "Fine-tuning outputs already exist. "
        "Move them to a backup directory or choose new output filenames:\n"
        + "\n".join(str(path) for path in existing_files)
    )

FINETUNED_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
# ============================================================
# 2. CHECK FILES AND DIRECTORIES
# ============================================================

if not os.path.exists(INITIAL_MODEL_PATH):
    raise FileNotFoundError(
        f"Initial model not found: {INITIAL_MODEL_PATH}"
    )

if not os.path.exists(CLASS_NAMES_PATH):
    raise FileNotFoundError(
        f"Class names file not found: {CLASS_NAMES_PATH}"
    )

if not os.path.isdir(TRAIN_DIR):
    raise FileNotFoundError(TRAIN_DIR)

if not os.path.isdir(VAL_DIR):
    raise FileNotFoundError(VAL_DIR)

print("=" * 65)
print("CATTLE VISION - 18 BREED MODEL FINE-TUNING")
print("=" * 65)

# ============================================================
# 3. LOAD CLASS NAMES
# ============================================================

with open(CLASS_NAMES_PATH, "r") as file:
    class_names = json.load(file)

if len(class_names) != NUM_CLASSES:
    raise ValueError(
        f"Expected {NUM_CLASSES} classes, found {len(class_names)}"
    )

print("\nClasses:", len(class_names))

# ============================================================
# 4. LOAD TRAINING DATASET
# ============================================================

train_dataset = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=True,
    seed=SEED
)

# ============================================================
# 5. LOAD VALIDATION DATASET
# ============================================================

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    VAL_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=False
)

# ============================================================
# 6. VERIFY CLASS ORDER
# ============================================================

if train_dataset.class_names != class_names:
    raise ValueError(
        "Training dataset class order does not match saved class names."
    )

if validation_dataset.class_names != class_names:
    raise ValueError(
        "Validation dataset class order does not match saved class names."
    )

print("\nClass order verified successfully.")

# ============================================================
# 7. DATASET OPTIMIZATION
# ============================================================

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(AUTOTUNE)
validation_dataset = validation_dataset.prefetch(AUTOTUNE)

# ============================================================
# 8. LOAD INITIAL TRAINED MODEL
# ============================================================

print("\nLoading initial trained model...")

model = tf.keras.models.load_model(
    INITIAL_MODEL_PATH
)

print("Initial model loaded successfully.")

# ============================================================
# 9. IDENTIFY MOBILENETV2 BASE MODEL
# ============================================================

base_model = None

for layer in model.layers:
    if isinstance(layer, tf.keras.Model) and len(layer.layers) > 100:
        base_model = layer
        break

if base_model is None:
    raise ValueError(
        "Could not identify the nested MobileNetV2 model."
    )

print("\nBase model identified:", base_model.name)
print("Total MobileNetV2 layers:", len(base_model.layers))

# ============================================================
# 10. UNFREEZE LAST 30 LAYERS
# ============================================================

base_model.trainable = True

# Freeze earlier layers

for layer in base_model.layers[:-UNFREEZE_LAST_LAYERS]:
    layer.trainable = False

# Unfreeze selected deeper layers, except BatchNormalization

for layer in base_model.layers[-UNFREEZE_LAST_LAYERS:]:
    if isinstance(layer, tf.keras.layers.BatchNormalization):
        layer.trainable = False
    else:
        layer.trainable = True

print("\nFine-tuning configuration:")
print("Unfrozen layer range: Last", UNFREEZE_LAST_LAYERS, "layers")
print("BatchNormalization layers remain frozen.")

trainable_layers = sum(
    1 for layer in base_model.layers if layer.trainable
)

print("Trainable base-model layers:", trainable_layers)

# ============================================================
# 11. RECOMPILE MODEL WITH LOWER LEARNING RATE
# ============================================================

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=LEARNING_RATE
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

print("\nModel recompiled successfully.")

# ============================================================
# 12. CALLBACKS
# ============================================================

checkpoint = ModelCheckpoint(
    filepath=FINETUNED_MODEL_PATH,
    monitor="val_accuracy",
    save_best_only=True,
    mode="max",
    verbose=1
)

early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=4,
    restore_best_weights=True,
    verbose=1
)

reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.2,
    patience=2,
    min_lr=0.000001,
    verbose=1
)

callbacks = [
    checkpoint,
    early_stopping,
    reduce_lr
]

# ============================================================
# 13. FINE-TUNE MODEL
# ============================================================

print("\n" + "=" * 65)
print("STARTING FINE-TUNING")
print("=" * 65)

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS,
    callbacks=callbacks
)

# ============================================================
# 14. SAVE FINE-TUNING HISTORY
# ============================================================

history_data = {
    key: [float(value) for value in values]
    for key, values in history.history.items()
}

with open(HISTORY_PATH, "w") as file:
    json.dump(history_data, file, indent=4)

print("\nFine-tuning history saved:", HISTORY_PATH)

# ============================================================
# 15. TRAINING RESULTS
# ============================================================

train_accuracy = history.history["accuracy"]
val_accuracy = history.history["val_accuracy"]

train_loss = history.history["loss"]
val_loss = history.history["val_loss"]

best_val_accuracy = max(val_accuracy)
best_epoch = val_accuracy.index(best_val_accuracy) + 1

print("\n" + "=" * 65)
print("FINE-TUNING RESULTS")
print("=" * 65)

print("Epochs completed:", len(train_accuracy))

print(
    f"Final training accuracy: "
    f"{train_accuracy[-1] * 100:.2f}%"
)

print(
    f"Final validation accuracy: "
    f"{val_accuracy[-1] * 100:.2f}%"
)

print(
    f"Best validation accuracy: "
    f"{best_val_accuracy * 100:.2f}%"
)

print("Best validation epoch:", best_epoch)

print(f"Final training loss: {train_loss[-1]:.4f}")
print(f"Final validation loss: {val_loss[-1]:.4f}")

print("\nFine-tuned model saved at:")
print(FINETUNED_MODEL_PATH)

# ============================================================
# 16. PLOT ACCURACY
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    train_accuracy,
    label="Training Accuracy"
)

plt.plot(
    val_accuracy,
    label="Validation Accuracy"
)

plt.title("MobileNetV2 - 18 Breed Fine-Tuning Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    BASE_DIR / "results" / "training" / "original_format" / "finetuning_accuracy_18breed.png",
    dpi=300
)

plt.show()

# ============================================================
# 17. PLOT LOSS
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    train_loss,
    label="Training Loss"
)

plt.plot(
    val_loss,
    label="Validation Loss"
)

plt.title("MobileNetV2 - 18 Breed Fine-Tuning Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    BASE_DIR / "results" / "training" / "original_format" / "finetuning_loss_18breed.png",
    dpi=300
)

plt.show()

print("\n" + "=" * 65)
print("FINE-TUNING COMPLETED")
print("=" * 65)