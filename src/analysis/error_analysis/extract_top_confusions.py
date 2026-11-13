import pandas as pd
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

CSV_PATH = (
    BASE_DIR
    / "results"
    / "error_analysis"
    / "24_breed"
    / "misclassified_images"
    / "misclassified_predictions.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "results"
    / "error_analysis"
    / "24_breed"
    / "confusion_review"
)

if not CSV_PATH.exists():
    raise FileNotFoundError(f"Missing input CSV: {CSV_PATH}")

if OUTPUT_DIR.exists() and any(OUTPUT_DIR.iterdir()):
    raise FileExistsError(
        f"Output directory already contains data: {OUTPUT_DIR}\n"
        "Refusing to overwrite existing confusion-review images."
    )

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV_PATH)

top_pairs = [
    ("Hallikar", "Ongole"),
    ("Kenkatha", "Kangayam"),
    ("ghumsari", "Shweta Kapila"),
    ("Poda Thirupu", "Dangi"),
    ("malvi", "Nari")
]

for actual, predicted in top_pairs:

    pair_name = f"{actual}_TO_{predicted}"

    pair_folder = OUTPUT_DIR / pair_name
    pair_folder.mkdir(parents=True, exist_ok=True)

    selected = df[
        (df["actual_breed"] == actual) &
        (df["predicted_breed"] == predicted)
    ]

    for _, row in selected.iterrows():

        source = Path(row["image_path"])

        destination = pair_folder / source.name

        shutil.copy2(source, destination)

    print(
        f"{actual} -> {predicted}: "
        f"{len(selected)} images extracted"
    )

print("\nImage extraction completed!")
