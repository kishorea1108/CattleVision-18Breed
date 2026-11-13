import pandas as pd
import numpy as np
import imagehash

from PIL import Image
from pathlib import Path

# ==========================================
# CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_DIR = BASE_DIR / "datasets" / "source" / "dataset_18breeds_cleaned"
OUTPUT_DIR = BASE_DIR / "results" / "duplicate_audit" / "18_breed" / "duplicate_audit_18breeds_final"

OUTPUT_DIR.mkdir(exist_ok=True)

HASH_THRESHOLD = 6

EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".webp"
}

# ==========================================
# COLLECT IMAGES
# ==========================================

records = []

for breed_folder in sorted(DATASET_DIR.iterdir()):

    if not breed_folder.is_dir():
        continue

    for image_path in breed_folder.iterdir():

        if image_path.suffix.lower() not in EXTENSIONS:
            continue

        records.append({
            "path": str(image_path),
            "filename": image_path.name,
            "breed": breed_folder.name
        })

print("Total images:", len(records))

# ==========================================
# CALCULATE PERCEPTUAL HASHES
# ==========================================

hashes = []
valid_records = []

print("\nCalculating perceptual hashes...")

for i, record in enumerate(records):

    try:
        with Image.open(record["path"]) as image:
            phash = imagehash.phash(image.convert("RGB"))

        hashes.append(int(str(phash), 16))
        valid_records.append(record)

    except Exception as error:
        print("Error:", record["path"], error)

    if (i + 1) % 500 == 0:
        print(f"Processed {i + 1}/{len(records)}")

# ==========================================
# COMPARE HASHES
# ==========================================

hash_array = np.array(hashes, dtype=np.uint64)

BIT_COUNTS = np.array(
    [bin(i).count("1") for i in range(256)],
    dtype=np.uint8
)

duplicate_pairs = []

total = len(hash_array)

print("\nComparing images...")

for i in range(total - 1):

    xor_values = np.bitwise_xor(
        hash_array[i + 1:],
        hash_array[i]
    )

    distances = BIT_COUNTS[
        xor_values.view(np.uint8).reshape(-1, 8)
    ].sum(axis=1)

    matches = np.where(
        distances <= HASH_THRESHOLD
    )[0]

    for match in matches:

        j = i + 1 + match

        image1 = valid_records[i]
        image2 = valid_records[j]

        duplicate_pairs.append({

            "image_1": image1["filename"],
            "image_2": image2["filename"],

            "breed_1": image1["breed"],
            "breed_2": image2["breed"],

            "hash_distance": int(distances[match]),

            "same_breed": (
                image1["breed"] == image2["breed"]
            ),

            "path_1": image1["path"],
            "path_2": image2["path"]
        })

    if (i + 1) % 500 == 0:
        print(f"Compared {i + 1}/{total}")

# ==========================================
# SAVE RESULTS
# ==========================================

columns = [
    "image_1",
    "image_2",
    "breed_1",
    "breed_2",
    "hash_distance",
    "same_breed",
    "path_1",
    "path_2"
]

df = pd.DataFrame(
    duplicate_pairs,
    columns=columns
)

if not df.empty:
    df = df.sort_values("hash_distance")

df.to_csv(
    OUTPUT_DIR / "duplicate_pairs.csv",
    index=False
)

# ==========================================
# SUMMARY
# ==========================================

print("\n========== 18-BREED AUDIT SUMMARY ==========")

print("Total valid images:", len(valid_records))
print("Potential duplicate pairs:", len(df))

if not df.empty:

    print("Same-breed pairs:", int(df["same_breed"].sum()))

    print("Cross-breed pairs:", int((~df["same_breed"]).sum()))

    print("\nTOP 20 MATCHES:\n")

    print(
        df.head(20)[
            [
                "image_1",
                "image_2",
                "breed_1",
                "breed_2",
                "hash_distance"
            ]
        ].to_string(index=False)
    )

print("\nReport saved:")
print(OUTPUT_DIR / "duplicate_pairs.csv")

print("\nAudit completed!")