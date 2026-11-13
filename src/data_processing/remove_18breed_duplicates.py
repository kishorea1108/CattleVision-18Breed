import shutil
import pandas as pd
from pathlib import Path

# ==========================================
# CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

SOURCE_DIR = BASE_DIR / "datasets" / "archive" / "dataset_18breeds"

OUTPUT_DIR = BASE_DIR / "datasets" / "source" / "dataset_18breeds_cleaned"

QUARANTINE_DIR = BASE_DIR / "results" / "duplicate_audit" / "18_breed" / "duplicate_quarantine_18breeds"
# ==========================================
# VERIFIED DUPLICATE PAIRS
# ==========================================

duplicate_pairs = [
    ("Kangayam", "Kangayam_144.jpg"),
    ("Pulikulam", "Pulikulam_062.jpg"),

    ("Pulikulam", "Pulikulam_082.png"),
    ("Umblachery", "Umblachery_211.png"),

    ("Pulikulam", "Pulikulam_066.jpg"),
    ("Umblachery", "Umblachery_104.png"),

    ("Dangi", "Dangi_067.webp"),
    ("ponwar", "ponwar_196.jpg"),

    ("Kangayam", "Kangayam_230.jpg"),
    ("Umblachery", "Umblachery_012.webp"),

    ("Hallikar", "Hallikar_0243.png"),
    ("siri", "siri_082.webp")
]

# ==========================================
# VALIDATE
# ==========================================

if not SOURCE_DIR.exists():
    raise FileNotFoundError(SOURCE_DIR)

if OUTPUT_DIR.exists() or QUARANTINE_DIR.exists():
    raise FileExistsError(
        "Output or quarantine folder already exists. "
        "Rename it before running this program."
    )

# Verify all files exist before copying anything
for breed, filename in duplicate_pairs:

    source = SOURCE_DIR / breed / filename

    if not source.is_file():
        raise FileNotFoundError(
            f"Missing duplicate image: {source}"
        )

# ==========================================
# CREATE CLEANED DATASET
# ==========================================

print("\nCreating cleaned dataset...")

shutil.copytree(SOURCE_DIR, OUTPUT_DIR)

# ==========================================
# QUARANTINE DUPLICATE IMAGES
# ==========================================

print("\nQuarantining duplicate images...")

records = []

for breed, filename in duplicate_pairs:

    source = SOURCE_DIR / breed / filename

    quarantine_breed = QUARANTINE_DIR / breed
    quarantine_breed.mkdir(parents=True, exist_ok=True)

    # Preserve a copy for recovery
    shutil.copy2(
        source,
        quarantine_breed / filename
    )

    # Remove from cleaned dataset only
    cleaned_file = OUTPUT_DIR / breed / filename
    cleaned_file.unlink()

    records.append({
        "breed": breed,
        "filename": filename,
        "original_path": str(source),
        "quarantine_path": str(
            quarantine_breed / filename
        ),
        "action": "QUARANTINED"
    })

    print("Removed from cleaned dataset:", filename)

# ==========================================
# SAVE CLEANING REPORT
# ==========================================

QUARANTINE_DIR.mkdir(exist_ok=True)

pd.DataFrame(records).to_csv(
    QUARANTINE_DIR / "removed_images.csv",
    index=False
)

# ==========================================
# VERIFY FINAL COUNTS
# ==========================================

total_images = 0

print("\n========== CLEANING SUMMARY ==========\n")

for breed_folder in sorted(OUTPUT_DIR.iterdir()):

    if not breed_folder.is_dir():
        continue

    count = len([
        f for f in breed_folder.iterdir()
        if f.is_file()
    ])

    total_images += count

    print(f"{breed_folder.name}: {count}")

print("\nImages removed:", len(records))
print("Remaining images:", total_images)

print("\nCleaned dataset:", OUTPUT_DIR)
print("Quarantined images:", QUARANTINE_DIR)

print("\nOriginal dataset remains unchanged.")
print("Cleaning completed successfully!")