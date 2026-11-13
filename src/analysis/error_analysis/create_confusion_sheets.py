from pathlib import Path
from PIL import Image, ImageDraw
import math

BASE_DIR = Path(__file__).resolve().parents[3]

INPUT_DIR = (
    BASE_DIR
    / "results"
    / "error_analysis"
    / "24_breed"
    / "confusion_review"
)

OUTPUT_DIR = (
    BASE_DIR
    / "results"
    / "error_analysis"
    / "24_breed"
    / "confusion_contact_sheets"
)

if not INPUT_DIR.exists():
    raise FileNotFoundError(f"Input directory not found: {INPUT_DIR}")

if OUTPUT_DIR.exists() and any(OUTPUT_DIR.iterdir()):
    raise FileExistsError(
        f"Output directory already contains data: {OUTPUT_DIR}\n"
        "Refusing to overwrite existing contact sheets."
    )

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

THUMB_WIDTH = 300
THUMB_HEIGHT = 230
LABEL_HEIGHT = 35
COLUMNS = 2

for folder in INPUT_DIR.iterdir():

    if not folder.is_dir():
        continue

    images = [
        p for p in folder.iterdir()
        if p.suffix.lower() in [".jpg", ".jpeg", ".png"]
    ]

    if not images:
        continue

    rows = math.ceil(len(images) / COLUMNS)

    sheet = Image.new(
        "RGB",
        (
            COLUMNS * THUMB_WIDTH,
            rows * (THUMB_HEIGHT + LABEL_HEIGHT)
        ),
        "white"
    )

    draw = ImageDraw.Draw(sheet)

    for index, image_path in enumerate(sorted(images)):

        image = Image.open(image_path).convert("RGB")
        image.thumbnail((THUMB_WIDTH, THUMB_HEIGHT))

        x = (index % COLUMNS) * THUMB_WIDTH
        y = (index // COLUMNS) * (THUMB_HEIGHT + LABEL_HEIGHT)

        paste_x = x + (THUMB_WIDTH - image.width) // 2
        paste_y = y + (THUMB_HEIGHT - image.height) // 2

        sheet.paste(image, (paste_x, paste_y))

        draw.text(
            (x + 5, y + THUMB_HEIGHT),
            image_path.name,
            fill="black"
        )

    output_path = OUTPUT_DIR / f"{folder.name}.jpg"

    sheet.save(output_path, quality=95)

    print("Created:", output_path)

print("\nAll contact sheets generated!")