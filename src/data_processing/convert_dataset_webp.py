import os
import shutil
from PIL import Image

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

SOURCE_DIR = BASE_DIR / "datasets" / "archive" / "dataset_18breeds_split"
OUTPUT_DIR = BASE_DIR / "datasets" / "active" / "dataset_18breeds_split_jpeg"

SPLITS = ["train", "validation", "test"]

SUPPORTED_FORMATS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp"
}

total_copied = 0
total_converted = 0
total_failed = 0

if OUTPUT_DIR.exists() and any(OUTPUT_DIR.iterdir()):
    raise FileExistsError(
        f"Output directory already contains data: {OUTPUT_DIR}\n"
        "Refusing to overwrite the existing dataset."
    )

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
print("=" * 65)
print("CATTLE VISION - WEBP CONVERSION")
print("=" * 65)

for split in SPLITS:

    source_split = os.path.join(SOURCE_DIR, split)
    output_split = os.path.join(OUTPUT_DIR, split)

    print(f"\nPROCESSING: {split.upper()}")

    for breed in sorted(os.listdir(source_split)):

        source_breed = os.path.join(source_split, breed)
        output_breed = os.path.join(output_split, breed)

        if not os.path.isdir(source_breed):
            continue

        os.makedirs(output_breed, exist_ok=True)

        for filename in os.listdir(source_breed):

            source_path = os.path.join(source_breed, filename)

            if not os.path.isfile(source_path):
                continue

            extension = os.path.splitext(filename)[1].lower()

            try:

                # Copy already supported image formats
                if extension in SUPPORTED_FORMATS:

                    destination = os.path.join(
                        output_breed,
                        filename
                    )

                    shutil.copy2(
                        source_path,
                        destination
                    )

                    total_copied += 1

                # Convert WebP to JPEG
                elif extension == ".webp":

                    new_filename = (
                        os.path.splitext(filename)[0]
                        + "__from_webp.jpg"
                    )

                    destination = os.path.join(
                        output_breed,
                        new_filename
                    )

                    with Image.open(source_path) as image:

                        image = image.convert("RGB")

                        image.save(
                            destination,
                            format="JPEG",
                            quality=95
                        )

                    total_converted += 1

                    print(
                        f"Converted: {breed}/{filename}"
                    )

                else:

                    print(
                        f"Unsupported format: {breed}/{filename}"
                    )

                    total_failed += 1

            except Exception as error:

                print(
                    f"FAILED: {breed}/{filename} - {error}"
                )

                total_failed += 1


# ============================================================
# VERIFY OUTPUT COUNTS
# ============================================================

print("\n" + "=" * 65)
print("CONVERSION SUMMARY")
print("=" * 65)

print("Images copied:", total_copied)
print("WebP converted:", total_converted)
print("Failed images:", total_failed)

grand_total = 0

for split in SPLITS:

    split_path = os.path.join(OUTPUT_DIR, split)

    split_total = 0

    for breed in os.listdir(split_path):

        breed_path = os.path.join(split_path, breed)

        if not os.path.isdir(breed_path):
            continue

        count = sum(
            1
            for filename in os.listdir(breed_path)
            if filename.lower().endswith(
                (".jpg", ".jpeg", ".png", ".bmp")
            )
        )

        split_total += count

    grand_total += split_total

    print(f"{split.upper()} TOTAL: {split_total}")

print("-" * 65)
print("TOTAL OUTPUT IMAGES:", grand_total)

if total_failed == 0 and grand_total == 3665:
    print("\nSUCCESS: All 3665 images are available.")
else:
    print("\nWARNING: Check the conversion results.")

print("=" * 65)