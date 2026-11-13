from backend.cattle_detector import detect_cattle
import json
from pathlib import Path
from io import BytesIO

import numpy as np
import tensorflow as tf

from PIL import Image, UnidentifiedImageError
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "final"
    / "mobilenetv2_18breed_finetuned_best.keras"
)

CLASS_NAMES_PATH = (
    BASE_DIR
    / "models"
    / "final"
    / "class_names_18breed.json"
)


# --------------------------------------------------
# APPLICATION INITIALIZATION
# --------------------------------------------------

app = FastAPI(
    title="CattleVision API",
    description="AI-based cattle breed identification using MobileNetV2",
    version="1.0.0",
)


# --------------------------------------------------
# CORS CONFIGURATION
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# MODEL LOADING
# --------------------------------------------------

print("Loading MobileNetV2 model...")

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

if not CLASS_NAMES_PATH.exists():
    raise FileNotFoundError(
        f"Class names file not found: {CLASS_NAMES_PATH}"
    )

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as file:
    class_names = json.load(file)

if len(class_names) != model.output_shape[-1]:
    raise ValueError(
        "Number of class names does not match model output."
    )

print("Model loaded successfully.")
print(f"Number of cattle breeds: {len(class_names)}")


# --------------------------------------------------
# IMAGE PREPROCESSING
# --------------------------------------------------

def preprocess_image(image_bytes: bytes):

    try:
        image = Image.open(BytesIO(image_bytes))

        image = image.convert("RGB")

        image = image.resize((224, 224))

        image_array = np.array(image, dtype=np.float32)

        image_array = np.expand_dims(image_array, axis=0)

        return image_array

    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Invalid or unsupported image file."
        )


# --------------------------------------------------
# HOME ENDPOINT
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Welcome to CattleVision API",
        "status": "Running",
        "model": "MobileNetV2",
        "supported_breeds": len(class_names),
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model_loaded": True,
        "number_of_breeds": len(class_names),
    }


# --------------------------------------------------
# BREED IDENTIFICATION ENDPOINT
# --------------------------------------------------
@app.post("/predict")
async def predict_breed(file: UploadFile = File(...)):

    # Validate file type
    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/webp",
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG and WEBP images are supported."
        )

    # Read uploaded image
    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty."
        )

    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Image size must not exceed 10 MB."
        )

    try:
        # STEP 1: Verify cattle presence using YOLO
        cattle_result = detect_cattle(image_bytes)

        if not cattle_result["cattle_detected"]:
            raise HTTPException(
                status_code=422,
                detail="No cattle detected. Please upload a clear image containing cattle."
            )

        # STEP 2: Preprocess image for MobileNetV2
        processed_image = preprocess_image(image_bytes)

        # STEP 3: Predict cattle breed
        predictions = model.predict(
            processed_image,
            verbose=0
        )

        scores = predictions[0]

        # Top 3 predictions
        top_indices = np.argsort(scores)[::-1][:3]

        top_predictions = []

        for index in top_indices:

            top_predictions.append({
                "breed": class_names[int(index)],
                "confidence": round(
                    float(scores[index]) * 100,
                    2
                ),
            })

        best_prediction = top_predictions[0]

        return {
            "success": True,
            "predicted_breed": best_prediction["breed"],
            "confidence": best_prediction["confidence"],
            "top_predictions": top_predictions,
            "cattle_detected": True,
            "detection_confidence": max(
                item["confidence"]
                for item in cattle_result["detections"]
            )
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )