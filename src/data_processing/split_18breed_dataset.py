import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split

# ==========================================
# CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

SOURCE_DIR = BASE_DIR / "datasets" / "source" / "dataset_18breeds_cleaned"
OUTPUT_DIR = BASE_DIR / "datasets" / "archive" / "dataset_18breeds_split"
SEED = 42

TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".webp"
}

# ==========================================
# VALIDATION
# ==========================================

if not SOURCE_DIR.exists():
    raise FileNotFoundError(SOURCE_DIR)

if OUTPUT_DIR.exists():
    raise FileExistsError(
        "Output folder already exists. Rename it first."
    )

assert abs(
    TRAIN_RATIO + VALIDATION_RATIO + TEST_RATIO - 1.0
) < 1e-9

OUTPUT_DIR.mkdir(parents=True)

# ==========================================
# CREATE SPLIT FOLDERS
# ==========================================

for split in ["train", "validation", "test"]:
    (OUTPUT_DIR / split).mkdir()

total_counts = {
    "train": 0,
    "validation": 0,
    "test": 0
}

# ==========================================
# STRATIFIED SPLITTING
# ==========================================

print("\n========== 18-BREED DATASET SPLITTING ==========\n")

for breed_folder in sorted(SOURCE_DIR.iterdir()):

    if not breed_folder.is_dir():
        continue

    images = sorted([
        p for p in breed_folder.iterdir()
        if p.is_file()
        and p.suffix.lower() in IMAGE_EXTENSIONS
    ])

    if len(images) < 3:
        raise ValueError(
            f"Insufficient images for breed: {breed_folder.name}"
        )

    train_images, remaining_images = train_test_split(
        images,
        train_size=TRAIN_RATIO,
        random_state=SEED
    )

    val_images, test_images = train_test_split(
        remaining_images,
        test_size=0.5,
        random_state=SEED
    )

    split_data = {
        "train": train_images,
        "validation": val_images,
        "test": test_images
    }

    for split_name, split_images in split_data.items():

        destination = (
            OUTPUT_DIR / split_name / breed_folder.name
        )

        destination.mkdir(parents=True, exist_ok=True)

        for image in split_images:
            shutil.copy2(
                image,
                destination / image.name
            )

        total_counts[split_name] += len(split_images)

    print(
        f"{breed_folder.name}: "
        f"Train={len(train_images)}, "
        f"Validation={len(val_images)}, "
        f"Test={len(test_images)}, "
        f"Total={len(images)}"
    )

# ==========================================
# FINAL SUMMARY
# ==========================================

print("\n========== FINAL SPLIT SUMMARY ==========")

for split, count in total_counts.items():

    percentage = count / sum(total_counts.values()) * 100

    print(f"{split}: {count} ({percentage:.2f}%)")

print("Total images:", sum(total_counts.values()))
print("Total breeds:", len([
    p for p in SOURCE_DIR.iterdir()
    if p.is_dir()
]))

print("\nOutput directory:", OUTPUT_DIR)
print("Dataset splitting completed!")