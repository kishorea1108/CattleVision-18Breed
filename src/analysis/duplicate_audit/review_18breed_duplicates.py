import pandas as pd
from PIL import Image, ImageDraw
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

CSV_PATH = (
    BASE_DIR
    / "results"
    / "duplicate_audit"
    / "18_breed"
    / "duplicate_audit_18breeds"
    / "duplicate_pairs.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "results"
    / "duplicate_audit"
    / "18_breed"
    / "duplicate_review_18breeds"
)

if OUTPUT_DIR.exists() and any(OUTPUT_DIR.iterdir()):
    raise FileExistsError(
        f"Output directory already contains data: {OUTPUT_DIR}\n"
        "Refusing to overwrite existing review images."
    )

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV_PATH)

WIDTH = 400
HEIGHT = 300
LABEL_HEIGHT = 60

for index, row in df.iterrows():

    canvas = Image.new(
        "RGB",
        (WIDTH * 2, HEIGHT + LABEL_HEIGHT),
        "white"
    )

    draw = ImageDraw.Draw(canvas)

    paths = [
        Path(row["path_1"]),
        Path(row["path_2"])
    ]

    for column, path in enumerate(paths):

        image = Image.open(path).convert("RGB")
        image.thumbnail((WIDTH - 10, HEIGHT - 10))

        x = column * WIDTH

        canvas.paste(
            image,
            (
                x + (WIDTH - image.width) // 2,
                (HEIGHT - image.height) // 2
            )
        )

        label = (
            f"{path.name}\n"
            f"Breed: {row[f'breed_{column + 1}']}"
        )

        draw.text(
            (x + 5, HEIGHT),
            label,
            fill="black"
        )

    draw.text(
        (5, 5),
        f"Pair {index + 1} | "
        f"Hash distance: {row['hash_distance']}",
        fill="red"
    )

    output_path = (
        OUTPUT_DIR / f"pair_{index + 1}.jpg"
    )

    canvas.save(output_path, quality=95)

    print("Created:", output_path)

print("\nAll six comparison images generated.")