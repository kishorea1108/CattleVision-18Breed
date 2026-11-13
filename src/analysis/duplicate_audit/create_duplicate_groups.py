import pandas as pd
from pathlib import Path
from collections import defaultdict

# ==========================================
# 1. CONFIGURATION
# ==========================================
BASE_DIR = Path(__file__).resolve().parents[3]

CSV_PATH = (
    BASE_DIR
    / "results"
    / "duplicate_audit"
    / "24_breed"
    / "duplicate_audit"
    / "perceptual_duplicate_pairs.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "results"
    / "duplicate_audit"
    / "24_breed"
    / "duplicate_verification"
)

if OUTPUT_DIR.exists() and any(OUTPUT_DIR.iterdir()):
    raise FileExistsError(
        f"Output directory already contains data: {OUTPUT_DIR}\n"
        "Refusing to overwrite existing verification results."
    )

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CSV_PATH = Path(
    "duplicate_audit/perceptual_duplicate_pairs.csv"
)

OUTPUT_DIR = Path("duplicate_verification")

OUTPUT_DIR.mkdir(exist_ok=True)

# ==========================================
# 2. LOAD DUPLICATE PAIRS
# ==========================================

df = pd.read_csv(CSV_PATH)

print("Potential duplicate pairs:", len(df))

# ==========================================
# 3. UNION-FIND
# ==========================================

parent = {}

def find(x):
    if x not in parent:
        parent[x] = x

    if parent[x] != x:
        parent[x] = find(parent[x])

    return parent[x]


def union(a, b):
    root_a = find(a)
    root_b = find(b)

    if root_a != root_b:
        parent[root_b] = root_a


# Connect images belonging to the same duplicate group
for _, row in df.iterrows():

    union(
        row["path_1"],
        row["path_2"]
    )

# ==========================================
# 4. BUILD GROUPS
# ==========================================

groups = defaultdict(list)

for image_path in parent:

    root = find(image_path)

    groups[root].append(image_path)

# Sort groups by size
sorted_groups = sorted(
    groups.values(),
    key=lambda x: (-len(x), sorted(x)[0])
)

# ==========================================
# 5. CREATE IMAGE METADATA
# ==========================================

image_metadata = {}

for _, row in df.iterrows():

    image_metadata[row["path_1"]] = {
        "filename": row["image_1"],
        "breed": row["breed_1"],
        "split": row["split_1"]
    }

    image_metadata[row["path_2"]] = {
        "filename": row["image_2"],
        "breed": row["breed_2"],
        "split": row["split_2"]
    }

# ==========================================
# 6. GENERATE REVIEW FILES
# ==========================================

group_records = []
image_records = []

for index, image_paths in enumerate(sorted_groups, start=1):

    group_id = f"GROUP_{index:03d}"

    breeds = set()
    splits = set()

    for image_path in sorted(image_paths):

        metadata = image_metadata[image_path]

        breeds.add(metadata["breed"])
        splits.add(metadata["split"])

        image_records.append({
            "group_id": group_id,
            "filename": metadata["filename"],
            "breed": metadata["breed"],
            "split": metadata["split"],
            "image_path": image_path
        })

    group_records.append({
        "group_id": group_id,
        "image_count": len(image_paths),
        "breeds": " | ".join(sorted(breeds)),
        "splits": " | ".join(sorted(splits)),
        "image_paths": " | ".join(sorted(image_paths)),
        "decision": "",
        "verified_correct_breed": "",
        "notes": ""
    })

# ==========================================
# 7. SAVE CSV FILES
# ==========================================

group_df = pd.DataFrame(group_records)

image_df = pd.DataFrame(image_records)

group_df.to_csv(
    OUTPUT_DIR / "group_review.csv",
    index=False
)

image_df.to_csv(
    OUTPUT_DIR / "group_images.csv",
    index=False
)

# ==========================================
# 8. PRINT SUMMARY
# ==========================================

print("\n========== DUPLICATE GROUP SUMMARY ==========")

print("Potential duplicate pairs:", len(df))
print("Connected duplicate groups:", len(groups))

print(
    "Total images involved:",
    len(image_df)
)

print("\nGROUP DETAILS:\n")

for group in group_records:

    print(
        f"{group['group_id']} | "
        f"Images: {group['image_count']} | "
        f"Breeds: {group['breeds']} | "
        f"Splits: {group['splits']}"
    )

print("\nFiles generated:")
print(OUTPUT_DIR / "group_review.csv")
print(OUTPUT_DIR / "group_images.csv")

print("\nVerification preparation completed!")