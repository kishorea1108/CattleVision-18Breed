import os
import numpy as np
import pandas as pd
import imagehash

from PIL import Image
from pathlib import Path

# ==========================================
# 1. CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[3]

DATASET_DIR = (
    BASE_DIR
    / "datasets"
    / "archive"
    / "dataset_split"
)

OUTPUT_DIR = (
    BASE_DIR
    / "results"
    / "duplicate_audit"
    / "24_breed"
    / "duplicate_audit"
)

if OUTPUT_DIR.exists() and any(OUTPUT_DIR.iterdir()):
    raise FileExistsError(
        f"Output directory already contains data: {OUTPUT_DIR}\n"
        "Refusing to overwrite existing audit results."
    )

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_FORMATS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".webp"
}

# Smaller threshold = stricter matching
# Start with 6 for a conservative audit.
HASH_THRESHOLD = 6

# ==========================================
# 2. COLLECT IMAGE INFORMATION
# ==========================================

image_records = []

print("\n========== PERCEPTUAL DUPLICATE AUDIT ==========\n")

for split in ["train", "validation", "test"]:

    split_dir = DATASET_DIR / split

    if not split_dir.exists():
        raise FileNotFoundError(f"Missing directory: {split_dir}")

    for breed_folder in sorted(split_dir.iterdir()):

        if not breed_folder.is_dir():
            continue

        for image_path in breed_folder.iterdir():

            if image_path.suffix.lower() not in SUPPORTED_FORMATS:
                continue

            image_records.append({
                "path": str(image_path),
                "filename": image_path.name,
                "split": split,
                "breed": breed_folder.name
            })

print("Total images found:", len(image_records))

# ==========================================
# 3. CALCULATE PERCEPTUAL HASHES
# ==========================================

hashes = []
valid_records = []

print("\nCalculating perceptual hashes...")

for index, record in enumerate(image_records):

    try:
        with Image.open(record["path"]) as image:
            image = image.convert("RGB")
            phash = imagehash.phash(image)

        hashes.append(int(str(phash), 16))
        valid_records.append(record)

    except Exception as error:
        print("Could not process:", record["path"])
        print("Error:", error)

    if (index + 1) % 500 == 0:
        print(f"Processed {index + 1}/{len(image_records)}")

print("Valid images:", len(valid_records))

# ==========================================
# 4. COMPARE PERCEPTUAL HASHES
# ==========================================

print("\nComparing image hashes...")

hash_array = np.array(hashes, dtype=np.uint64)

# Lookup table for counting set bits
BIT_COUNTS = np.array(
    [bin(i).count("1") for i in range(256)],
    dtype=np.uint8
)

duplicate_pairs = []

total = len(hash_array)

for i in range(total - 1):

    xor_values = np.bitwise_xor(
        hash_array[i + 1:],
        hash_array[i]
    )

    # Count differing bits
    distances = BIT_COUNTS[
        xor_values.view(np.uint8).reshape(-1, 8)
    ].sum(axis=1)

    matches = np.where(distances <= HASH_THRESHOLD)[0]

    for match in matches:

        j = i + 1 + match

        record1 = valid_records[i]
        record2 = valid_records[j]

        distance = int(distances[match])

        duplicate_pairs.append({
            "image_1": record1["filename"],
            "image_2": record2["filename"],

            "breed_1": record1["breed"],
            "breed_2": record2["breed"],

            "split_1": record1["split"],
            "split_2": record2["split"],

            "hash_distance": distance,

            "same_breed": (
                record1["breed"] == record2["breed"]
            ),

            "same_split": (
                record1["split"] == record2["split"]
            ),

            "cross_breed": (
                record1["breed"] != record2["breed"]
            ),

            "cross_split": (
                record1["split"] != record2["split"]
            ),

            "path_1": record1["path"],
            "path_2": record2["path"]
        })

    if (i + 1) % 500 == 0:
        print(f"Compared {i + 1}/{total} images")

# ==========================================
# 5. SAVE RESULTS
# ==========================================

columns = [
    "image_1", "image_2",
    "breed_1", "breed_2",
    "split_1", "split_2",
    "hash_distance",
    "same_breed", "same_split",
    "cross_breed", "cross_split",
    "path_1", "path_2"
]

df = pd.DataFrame(duplicate_pairs, columns=columns)

if not df.empty:

    df = df.sort_values(
        by="hash_distance",
        ascending=True
    )

df.to_csv(
    OUTPUT_DIR / "perceptual_duplicate_pairs.csv",
    index=False
)

# ==========================================
# 6. GENERATE SUMMARY
# ==========================================

print("\n========== AUDIT SUMMARY ==========")

print("Total valid images:", len(valid_records))
print("Potential duplicate pairs:", len(df))

if not df.empty:

    print(
        "Same-breed pairs:",
        int(df["same_breed"].sum())
    )

    print(
        "Cross-breed pairs:",
        int(df["cross_breed"].sum())
    )

    print(
        "Same-split pairs:",
        int(df["same_split"].sum())
    )

    print(
        "Cross-split pairs:",
        int(df["cross_split"].sum())
    )

    print("\nTOP 20 POTENTIAL DUPLICATES:\n")

    print(
        df.head(20)[
            [
                "image_1",
                "image_2",
                "breed_1",
                "breed_2",
                "split_1",
                "split_2",
                "hash_distance"
            ]
        ].to_string(index=False)
    )

else:
    print("No potential duplicates detected.")

print("\nReport saved at:")
print(OUTPUT_DIR / "perceptual_duplicate_pairs.csv")

print("\nAudit completed!")