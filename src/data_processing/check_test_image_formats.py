import os
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
TEST_DIR = BASE_DIR / "datasets" / "active" / "dataset_18breeds_split_jpeg" / "test"

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp"
}

print("=" * 65)
print("TEST DATASET IMAGE FORMAT ANALYSIS")
print("=" * 65)

total_images = 0
unsupported_images = []

for breed in sorted(os.listdir(TEST_DIR)):

    breed_path = os.path.join(TEST_DIR, breed)

    if not os.path.isdir(breed_path):
        continue

    extension_counts = Counter()

    for filename in os.listdir(breed_path):

        filepath = os.path.join(breed_path, filename)

        if not os.path.isfile(filepath):
            continue

        extension = os.path.splitext(filename)[1].lower()

        extension_counts[extension] += 1
        total_images += 1

        if extension not in SUPPORTED_EXTENSIONS:
            unsupported_images.append(
                (breed, filename, extension)
            )

    print(f"\n{breed}")
    for extension, count in sorted(extension_counts.items()):
        print(f"  {extension or '[no extension]'} : {count}")

print("\n" + "=" * 65)
print("TOTAL TEST IMAGES:", total_images)
print("UNSUPPORTED FORMAT IMAGES:", len(unsupported_images))
print("=" * 65)

for breed, filename, extension in unsupported_images:
    print(f"{breed}/{filename} ({extension})")