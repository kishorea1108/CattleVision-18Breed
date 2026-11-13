import shutil
from pathlib import Path

# ==========================================
# 1. CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

SOURCE_DIR = BASE_DIR / "datasets" / "source" / "dataset_final"
OUTPUT_DIR = BASE_DIR / "datasets" / "archive" / "dataset_18breeds"

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".webp"
}

# ==========================================
# 2. SELECTED 18 BREEDS
# ==========================================

SELECTED_BREEDS = [
    "Bargur",
    "Dangi",
    "Gir",
    "Hallikar",
    "Himachali Pahari",
    "Kangayam",
    "Mewati",
    "Nari",
    "Ongole",
    "Poda Thirupu",
    "Pulikulam",
    "Purnea",
    "Red kandhari",
    "motu",
    "ponwar",
    "siri",
    "Tharparkar",
    "Umblachery"
]

# ==========================================
# 3. VALIDATE SOURCE
# ==========================================

if not SOURCE_DIR.exists():
    raise FileNotFoundError(
        f"Source dataset not found: {SOURCE_DIR}"
    )

if OUTPUT_DIR.exists():
    raise FileExistsError(
        f"{OUTPUT_DIR} already exists. "
        "Rename or remove it before running this script."
    )

# ==========================================
# 4. COPY SELECTED BREEDS
# ==========================================

OUTPUT_DIR.mkdir(parents=True)

total_images = 0

print("\n========== CREATING 18-BREED DATASET ==========\n")

for breed in SELECTED_BREEDS:

    source_breed = SOURCE_DIR / breed
    destination_breed = OUTPUT_DIR / breed

    if not source_breed.exists():
        raise FileNotFoundError(
            f"Missing breed folder: {source_breed}"
        )

    destination_breed.mkdir()

    images = [
        file for file in source_breed.iterdir()
        if file.is_file()
        and file.suffix.lower() in IMAGE_EXTENSIONS
    ]

    for image in images:
        shutil.copy2(
            image,
            destination_breed / image.name
        )

    count = len(images)
    total_images += count

    print(f"{breed}: {count} images")

# ==========================================
# 5. FINAL SUMMARY
# ==========================================

print("\n========== DATASET SUMMARY ==========")

print("Selected breeds:", len(SELECTED_BREEDS))
print("Total images:", total_images)
print("Output directory:", OUTPUT_DIR)

print("\n18-breed dataset created successfully!")

print("\nOriginal dataset_final remains unchanged.")