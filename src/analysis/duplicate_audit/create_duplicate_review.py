import pandas as pd
from PIL import Image, ImageDraw
from pathlib import Path
import math

# ==========================================
# CONFIGURATION
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
    / "duplicate_review"
)

if OUTPUT_DIR.exists() and any(OUTPUT_DIR.iterdir()):
    raise FileExistsError(
        f"Output directory already contains data: {OUTPUT_DIR}\n"
        "Refusing to overwrite existing review images."
    )

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

IMAGE_WIDTH = 220
IMAGE_HEIGHT = 160
LABEL_HEIGHT = 65

PAIRS_PER_SHEET = 6

# ==========================================
# LOAD CSV
# ==========================================

df = pd.read_csv(CSV_PATH)

# Sort by hash distance
df = df.sort_values(
    "hash_distance",
    ascending=True
).reset_index(drop=True)

print("Total pairs:", len(df))

# ==========================================
# CREATE COMPARISON SHEETS
# ==========================================

for start in range(0, len(df), PAIRS_PER_SHEET):

    subset = df.iloc[
        start:start + PAIRS_PER_SHEET
    ]

    rows = len(subset)

    sheet = Image.new(
        "RGB",
        (
            IMAGE_WIDTH * 2,
            rows * (IMAGE_HEIGHT + LABEL_HEIGHT)
        ),
        "white"
    )

    draw = ImageDraw.Draw(sheet)

    for position, (_, row) in enumerate(subset.iterrows()):

        y = position * (IMAGE_HEIGHT + LABEL_HEIGHT)

        paths = [
            Path(row["path_1"]),
            Path(row["path_2"])
        ]

        labels = [
            f"Image 1: {row['breed_1']} | {row['split_1']}",
            f"Image 2: {row['breed_2']} | {row['split_2']}"
        ]

        for col in range(2):

            image = Image.open(paths[col]).convert("RGB")

            image.thumbnail(
                (IMAGE_WIDTH - 10, IMAGE_HEIGHT - 10)
            )

            x = col * IMAGE_WIDTH

            px = x + (IMAGE_WIDTH - image.width) // 2
            py = y + (IMAGE_HEIGHT - image.height) // 2

            sheet.paste(image, (px, py))

            draw.text(
                (x + 5, y + IMAGE_HEIGHT),
                labels[col],
                fill="black"
            )

            draw.text(
                (x + 5, y + IMAGE_HEIGHT + 20),
                paths[col].name,
                fill="black"
            )

        draw.text(
            (5, y + IMAGE_HEIGHT + 40),
            f"Pair {start + position + 1} | "
            f"Hash distance: {row['hash_distance']}",
            fill="red"
        )

    sheet_number = start // PAIRS_PER_SHEET + 1

    output_path = (
        OUTPUT_DIR /
        f"duplicate_review_{sheet_number}.jpg"
    )

    sheet.save(output_path, quality=95)

    print("Created:", output_path)

print("\nAll comparison sheets generated!")