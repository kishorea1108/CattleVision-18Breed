
import os
import json
import tensorflow as tf
import matplotlib.pyplot as plt
from pathlib import Path
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.callbacks import (
    ModelCheckpoint,
    EarlyStopping,
    ReduceLROnPlateau
)

# ============================================================
# 1. CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

TRAIN_DIR = BASE_DIR / "datasets" / "active" / "dataset_18breeds_split_jpeg" / "train"
VAL_DIR = BASE_DIR / "datasets" / "active" / "dataset_18breeds_split_jpeg" / "validation"

MODEL_DIR = BASE_DIR / "models" / "experiments" / "all_formats"

MODEL_PATH = MODEL_DIR / "mobilenetv2_18breed_allformats_best.keras"

CLASS_NAMES_PATH = MODEL_DIR / "class_names_18breed_allformats.json"

HISTORY_PATH = MODEL_DIR / "training_history_18breed_allformats.json"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 20
NUM_CLASSES = 18
SEED = 42

MODEL_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 2. CHECK DATASET DIRECTORIES
# ============================================================

if not os.path.isdir(TRAIN_DIR):
    raise FileNotFoundError(f"Training directory not found: {TRAIN_DIR}")

if not os.path.isdir(VAL_DIR):
    raise FileNotFoundError(f"Validation directory not found: {VAL_DIR}")

print("=" * 65)
print("CATTLE VISION - 18 BREED CLASSIFICATION")
print("=" * 65)

# ============================================================
# 3. LOAD TRAINING DATASET
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
# 4. LOAD VALIDATION DATASET
# ============================================================

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    VAL_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=False
)

# ============================================================
# 5. VERIFY CLASS NAMES
# ============================================================

class_names = train_dataset.class_names
validation_class_names = validation_dataset.class_names

if class_names != validation_class_names:
    raise ValueError(
        "Training and validation class orders do not match!"
    )

if len(class_names) != NUM_CLASSES:
    raise ValueError(
        f"Expected {NUM_CLASSES} classes, found {len(class_names)}"
    )

print("\nTotal Classes:", len(class_names))

for index, breed in enumerate(class_names):
    print(f"{index + 1:02d}. {breed}")

# Save class names

with open(CLASS_NAMES_PATH, "w") as file:
    json.dump(class_names, file, indent=4)

print("\nClass names saved:", CLASS_NAMES_PATH)

# ============================================================
# 6. DATASET PERFORMANCE OPTIMIZATION
# ============================================================

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(
    buffer_size=AUTOTUNE
)

validation_dataset = validation_dataset.prefetch(
    buffer_size=AUTOTUNE
)

# ============================================================
# 7. DATA AUGMENTATION
# ============================================================

data_augmentation = tf.keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.08),
        layers.RandomZoom(0.1)
    ],
    name="data_augmentation"
)

# ============================================================
# 8. LOAD MOBILENETV2 PRETRAINED MODEL
# ============================================================

base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze pretrained layers

base_model.trainable = False

print("\nMobileNetV2 loaded successfully.")
print("Pretrained layers frozen.")

# ============================================================
# 9. BUILD COMPLETE MODEL
# ============================================================

inputs = layers.Input(
    shape=(224, 224, 3),
    name="input_image"
)

# Data augmentation

x = data_augmentation(inputs)

# MobileNetV2 preprocessing: convert pixels to [-1, 1]

x = layers.Rescaling(
    scale=1.0 / 127.5,
    offset=-1,
    name="mobilenetv2_preprocessing"
)(x)

# Feature extraction

x = base_model(
    x,
    training=False
)

# Classification head

x = layers.GlobalAveragePooling2D(
    name="global_average_pooling"
)(x)

x = layers.Dropout(
    0.3,
    name="dropout"
)(x)

outputs = layers.Dense(
    NUM_CLASSES,
    activation="softmax",
    name="breed_prediction"
)(x)

model = models.Model(
    inputs=inputs,
    outputs=outputs,
    name="CattleVision_MobileNetV2_18Breeds"
)

# ============================================================
# 10. COMPILE MODEL
# ============================================================

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

print("\nModel compiled successfully.")

model.summary()

# ============================================================
# 11. CALLBACKS
# ============================================================

checkpoint = ModelCheckpoint(
    filepath=MODEL_PATH,
    monitor="val_accuracy",
    save_best_only=True,
    mode="max",
    verbose=1
)

early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True,
    verbose=1
)

reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.2,
    patience=2,
    min_lr=0.00001,
    verbose=1
)

callbacks = [
    checkpoint,
    early_stopping,
    reduce_lr
]

# ============================================================
# 12. TRAIN MODEL
# ============================================================

print("\n" + "=" * 65)
print("STARTING MOBILENETV2 TRAINING - 18 BREEDS")
print("=" * 65)

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS,
    callbacks=callbacks
)

# ============================================================
# 13. SAVE TRAINING HISTORY
# ============================================================

history_data = {
    key: [float(value) for value in values]
    for key, values in history.history.items()
}

with open(HISTORY_PATH, "w") as file:
    json.dump(history_data, file, indent=4)

print("\nTraining history saved:", HISTORY_PATH)

# ============================================================
# 14. TRAINING RESULTS
# ============================================================

train_accuracy = history.history["accuracy"]
val_accuracy = history.history["val_accuracy"]

train_loss = history.history["loss"]
val_loss = history.history["val_loss"]

best_val_accuracy = max(val_accuracy)
best_val_epoch = val_accuracy.index(best_val_accuracy) + 1

final_train_accuracy = train_accuracy[-1]
final_val_accuracy = val_accuracy[-1]

final_train_loss = train_loss[-1]
final_val_loss = val_loss[-1]

print("\n" + "=" * 65)
print("TRAINING RESULTS")
print("=" * 65)

print(f"Epochs completed       : {len(train_accuracy)}")
print(f"Final training accuracy: {final_train_accuracy * 100:.2f}%")
print(f"Final validation acc.  : {final_val_accuracy * 100:.2f}%")
print(f"Best validation acc.   : {best_val_accuracy * 100:.2f}%")
print(f"Best validation epoch  : {best_val_epoch}")
print(f"Final training loss    : {final_train_loss:.4f}")
print(f"Final validation loss  : {final_val_loss:.4f}")

print("\nBest model saved at:", MODEL_PATH)

# ============================================================
# 15. PLOT TRAINING ACCURACY
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

plt.title("MobileNetV2 - 18 Breed Training Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    BASE_DIR / "results" / "training" / "all_formats" / "accuracy_18breed.png",
    dpi=300
)

plt.show()

# ============================================================
# 16. PLOT TRAINING LOSS
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

plt.title("MobileNetV2 - 18 Breed Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    BASE_DIR / "results" / "training" / "all_formats" / "loss_18breed.png",
    dpi=300
)

plt.show()

print("\n" + "=" * 65)
print("18-BREED TRAINING COMPLETED SUCCESSFULLY")
print("=" * 65)