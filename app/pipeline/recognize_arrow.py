import numpy as np
import supervision as sv

from ultralytics import YOLO

from config.path_config import get_arrow_detection_model_path

LOCAL_MODEL = YOLO(get_arrow_detection_model_path())

# Function to load configuration (can be moved to a central utils.py if used elsewhere)
# For now, keep it simple. The main caller (notebook) will load and pass the config.

def detect_arrowheads(
    image: np.ndarray,
    config: dict, # Expects the full loaded YAML config
) -> dict:
    # Get confidence threshold from config (now directly under connection_processing)
    connection_config = config.get('connection_processing', {})
    confidence_threshold = connection_config.get('arrowhead_confidence_threshold_percent', 10.0) / 100.0 # Default if not found

    img = image.copy()
    h, w = img.shape[:2]

    results = LOCAL_MODEL(img, conf=confidence_threshold)[0]

    predictions = []
    for box in results.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        w_box = x2 - x1
        h_box = y2 - y1
        cx = x1 + w_box / 2
        cy = y1 + h_box / 2

        predictions.append({
            "x": float(cx),
            "y": float(cy),
            "width": float(w_box),
            "height": float(h_box),
            "confidence": float(box.conf[0]),
            "class": LOCAL_MODEL.names[int(box.cls[0])],
            "class_id": int(box.cls[0])
        })

    return {
        "predictions": predictions,
        "image": {
            "width": w,
            "height": h
        }
    }

def show_arrows(img, arrowhead_result):
    img_drawn = img.copy()
    detections = sv.Detections.from_inference(arrowhead_result)

    # create supervision annotators
    bounding_box_annotator = sv.BoxAnnotator()

    # annotate the image with our inference results
    annotated_image = bounding_box_annotator.annotate(
        scene=img_drawn, detections=detections)

    sv.plot_image(annotated_image)