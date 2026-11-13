import hashlib
import imagehash
import numpy as np
import pandas as pd

from PIL import Image
from pathlib import Path

# ==========================================
# CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_DIR = (
    BASE_DIR
    / "datasets"
    / "active"
    / "dataset_18breeds_split_jpeg"
)

OUTPUT_DIR = (
    BASE_DIR
    / "results"
    / "leakage_audit"
    / "18_breed"
    / "leakage_audit_18breeds"
)

if OUTPUT_DIR.exists() and any(OUTPUT_DIR.iterdir()):
    raise FileExistsError(
        f"Output directory already contains results: {OUTPUT_DIR}. "
        "Choose a new output directory to preserve existing audit results."
    )

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SPLITS = ["train", "validation", "test"]

EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".webp"
}

HASH_THRESHOLD = 6

# ==========================================
# COLLECT IMAGE INFORMATION
# ==========================================

records = []

for split in SPLITS:

    split_dir = DATASET_DIR / split

    if not split_dir.exists():
        raise FileNotFoundError(split_dir)

    for breed_folder in sorted(split_dir.iterdir()):

        if not breed_folder.is_dir():
            continue

        for image_path in breed_folder.iterdir():

            if image_path.suffix.lower() not in EXTENSIONS:
                continue

            records.append({
                "path": str(image_path),
                "filename": image_path.name,
                "breed": breed_folder.name,
                "split": split
            })

print("Total images:", len(records))

# ==========================================
# SHA-256 AUDIT
# ==========================================

print("\n========== SHA-256 AUDIT ==========")

sha_records = []

for record in records:

    with open(record["path"], "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()

    sha_records.append({
        **record,
        "sha256": digest
    })

sha_df = pd.DataFrame(sha_records)

sha_duplicates = []

for digest, group in sha_df.groupby("sha256"):

    if group["split"].nunique() > 1:

        sha_duplicates.append(group)

if sha_duplicates:

    result = pd.concat(sha_duplicates)

    result.to_csv(
        OUTPUT_DIR / "sha256_leakage.csv",
        index=False
    )

    print("Cross-split exact duplicate groups:",
          len(sha_duplicates))

else:
    print("Cross-split exact duplicates: 0")

# ==========================================
# PERCEPTUAL HASH AUDIT
# ==========================================

print("\n========== PERCEPTUAL HASH AUDIT ==========")

hashes = []
valid_records = []

for index, record in enumerate(records):

    try:

        with Image.open(record["path"]) as image:

            phash = imagehash.phash(
                image.convert("RGB")
            )

        hashes.append(int(str(phash), 16))
        valid_records.append(record)

    except Exception as error:

        print("Image error:", record["path"], error)

    if (index + 1) % 500 == 0:
        print(f"Processed {index + 1}/{len(records)}")

hash_array = np.array(hashes, dtype=np.uint64)

BIT_COUNTS = np.array(
    [bin(i).count("1") for i in range(256)],
    dtype=np.uint8
)

leakage_pairs = []

total = len(hash_array)

for i in range(total - 1):

    # Compare only images from different splits
    candidate_indices = np.arange(i + 1, total)

    mask = np.array([
        valid_records[j]["split"] != valid_records[i]["split"]
        for j in candidate_indices
    ])

    candidate_indices = candidate_indices[mask]

    if len(candidate_indices) == 0:
        continue

    xor_values = np.bitwise_xor(
        hash_array[candidate_indices],
        hash_array[i]
    )

    distances = BIT_COUNTS[
        xor_values.view(np.uint8).reshape(-1, 8)
    ].sum(axis=1)

    matches = np.where(
        distances <= HASH_THRESHOLD
    )[0]

    for match in matches:

        j = candidate_indices[match]

        leakage_pairs.append({

            "image_1": valid_records[i]["filename"],
            "image_2": valid_records[j]["filename"],

            "breed_1": valid_records[i]["breed"],
            "breed_2": valid_records[j]["breed"],

            "split_1": valid_records[i]["split"],
            "split_2": valid_records[j]["split"],

            "hash_distance": int(distances[match]),

            "path_1": valid_records[i]["path"],
            "path_2": valid_records[j]["path"]
        })

    if (i + 1) % 500 == 0:
        print(f"Compared {i + 1}/{total}")

# ==========================================
# SAVE PERCEPTUAL RESULTS
# ==========================================

columns = [
    "image_1", "image_2",
    "breed_1", "breed_2",
    "split_1", "split_2",
    "hash_distance",
    "path_1", "path_2"
]

leakage_df = pd.DataFrame(
    leakage_pairs,
    columns=columns
)

leakage_df.to_csv(
    OUTPUT_DIR / "perceptual_leakage.csv",
    index=False
)

# ==========================================
# FINAL SUMMARY
# ==========================================

print("\n========== FINAL LEAKAGE AUDIT ==========")

print("Total images:", len(records))
print("Valid perceptual hashes:", len(valid_records))

print("SHA-256 cross-split duplicates:",
      sum(
          group["split"].nunique() > 1
          for _, group in sha_df.groupby("sha256")
      )
)

print("Perceptual cross-split pairs:",
      len(leakage_df))

if leakage_df.empty:

    print("\nNo potential cross-split perceptual duplicates detected.")

else:

    print("\nPotential leakage pairs found:\n")

    print(
        leakage_df.head(20).to_string(index=False)
    )

print("\nReports saved in:", OUTPUT_DIR)
print("\nAudit completed!")