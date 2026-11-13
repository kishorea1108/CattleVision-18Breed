import cv2
import numpy as np
import onnxruntime as ort


# Model configuration
MODEL_PATH = "models/detection/yolo11n.onnx"

INPUT_SIZE = 640
COW_CLASS_ID = 19

CONFIDENCE_THRESHOLD = 0.25
NMS_THRESHOLD = 0.45


# Load YOLO ONNX model
session = ort.InferenceSession(
    MODEL_PATH,
    providers=["CPUExecutionProvider"]
)

input_name = session.get_inputs()[0].name


def detect_cattle(image_bytes):

    # Decode uploaded image
    image_array = np.frombuffer(
        image_bytes,
        dtype=np.uint8
    )

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if image is None:
        raise ValueError("Invalid image.")

    original_height, original_width = image.shape[:2]

    # Letterbox preprocessing
    scale = min(
        INPUT_SIZE / original_width,
        INPUT_SIZE / original_height
    )

    new_width = int(round(original_width * scale))
    new_height = int(round(original_height * scale))

    resized = cv2.resize(
        image,
        (new_width, new_height)
    )

    canvas = np.full(
        (INPUT_SIZE, INPUT_SIZE, 3),
        114,
        dtype=np.uint8
    )

    pad_x = (INPUT_SIZE - new_width) // 2
    pad_y = (INPUT_SIZE - new_height) // 2

    canvas[
        pad_y:pad_y + new_height,
        pad_x:pad_x + new_width
    ] = resized

    # BGR to RGB
    canvas = cv2.cvtColor(
        canvas,
        cv2.COLOR_BGR2RGB
    )

    # Normalize and convert to NCHW
    input_tensor = canvas.astype(
        np.float32
    ) / 255.0

    input_tensor = np.transpose(
        input_tensor,
        (2, 0, 1)
    )

    input_tensor = np.expand_dims(
        input_tensor,
        axis=0
    )

    # YOLO inference
    outputs = session.run(
        None,
        {input_name: input_tensor}
    )

    predictions = outputs[0][0].T

    boxes = []
    confidences = []

    # Extract cow detections
    for detection in predictions:

        class_scores = detection[4:]

        confidence = float(
            class_scores[COW_CLASS_ID]
        )

        if confidence < CONFIDENCE_THRESHOLD:
            continue

        center_x, center_y, width, height = detection[:4]

        x1 = center_x - width / 2
        y1 = center_y - height / 2

        box_width = width
        box_height = height

        # Remove letterbox padding and restore coordinates
        x1 = (x1 - pad_x) / scale
        y1 = (y1 - pad_y) / scale

        box_width /= scale
        box_height /= scale

        # Clip coordinates to original image
        x1 = max(0, min(int(x1), original_width))
        y1 = max(0, min(int(y1), original_height))

        box_width = min(
            int(box_width),
            original_width - x1
        )

        box_height = min(
            int(box_height),
            original_height - y1
        )

        if box_width <= 0 or box_height <= 0:
            continue

        boxes.append([
            x1,
            y1,
            box_width,
            box_height
        ])

        confidences.append(confidence)

    # Non-Maximum Suppression
    indices = cv2.dnn.NMSBoxes(
        boxes,
        confidences,
        CONFIDENCE_THRESHOLD,
        NMS_THRESHOLD
    )

    detections = []

    if len(indices) > 0:

        for index in np.array(indices).flatten():

            detections.append({
                "class": "cow",
                "confidence": round(
                    confidences[index] * 100,
                    2
                ),
                "box": boxes[index]
            })

    return {
        "cattle_detected": len(detections) > 0,
        "detections": detections
    }