import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BASE_DIR = (
    PROJECT_ROOT
    / "datasets"
    / "active"
    / "dataset_18breeds_split_jpeg"
)

SPLITS = ["train", "validation", "test"]

IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp"
)

total_images = 0

print("=" * 65)
print("18-BREED DATASET COUNT VERIFICATION")
print("=" * 65)

for split in SPLITS:

    split_path = os.path.join(BASE_DIR, split)

    print(f"\n{split.upper()} DATASET")
    print("-" * 50)

    split_total = 0

    for breed in sorted(os.listdir(split_path)):

        breed_path = os.path.join(split_path, breed)

        if not os.path.isdir(breed_path):
            continue

        images = [
            file for file in os.listdir(breed_path)
            if file.lower().endswith(IMAGE_EXTENSIONS)
        ]

        count = len(images)

        split_total += count

        print(f"{breed:<25} : {count}")

    print("-" * 50)
    print(f"{split.upper()} TOTAL : {split_total}")

    total_images += split_total

print("\n" + "=" * 65)
print("TOTAL DATASET IMAGES:", total_images)
print("=" * 65)