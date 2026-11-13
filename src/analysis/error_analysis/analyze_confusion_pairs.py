import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

OUTPUT_DIR = (
    BASE_DIR
    / "results"
    / "error_analysis"
    / "24_breed"
    / "misclassified_images"
)

CSV_PATH = OUTPUT_DIR / "misclassified_predictions.csv"

if not CSV_PATH.exists():
    raise FileNotFoundError(f"Missing input CSV: {CSV_PATH}")

df = pd.read_csv(CSV_PATH)

# Count actual breed vs predicted breed combinations
confusion_pairs = (
    df.groupby(["actual_breed", "predicted_breed"])
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
)

print("\n========== TOP 20 CONFUSION PAIRS ==========\n")

print(confusion_pairs.head(20).to_string(index=False))

# Save results to a separate file to preserve existing results
OUTPUT_PATH = OUTPUT_DIR / "confusion_pairs_reorganized.csv"

if OUTPUT_PATH.exists():
    raise FileExistsError(
        f"Output file already exists: {OUTPUT_PATH}\n"
        "Refusing to overwrite it."
    )

confusion_pairs.to_csv(OUTPUT_PATH, index=False)

print("\nSaved:", OUTPUT_PATH)