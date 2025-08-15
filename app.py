from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import cv2
import os
import time
import numpy as np
import base64
from datetime import datetime

app = Flask(__name__, 
            template_folder='ui/templates',
            static_folder='ui/static')

# === CONFIGURATION ===
MODEL_PATH = 'models/best.pt'  # Path to your YOLO model
CONFIDENCE_THRESHOLD = 0.25

# === CLASSES (modify for your dataset) ===
CLASS_NAMES = ['cavity', 'normal']  # index 0 = cavity, index 1 = normal

# === Load YOLO model ===
try:
    model = YOLO(MODEL_PATH)
    print(f"✅ Model loaded from {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None


def predict_with_yolo(image_data_or_path, conf_threshold=0.25):
    """
    Run YOLO prediction and return annotated image + detection data
    """
    if model is None:
        raise Exception("Model not loaded")

    # If image_data_or_path is a path (e.g., temporary file for YOLO)
    if isinstance(image_data_or_path, str) and os.path.exists(image_data_or_path):
        img_bgr = cv2.imread(image_data_or_path)
    else: # Assume it's in-memory data if not a valid path
        nparr = np.frombuffer(image_data_or_path, np.uint8)
        img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img_bgr is None:
        raise Exception("Could not load image")

    original_size = (img_bgr.shape[1], img_bgr.shape[0])

    # YOLO prediction
    start_time = time.time()
    # Pass image directly to model.predict if it supports in-memory, otherwise save temporarily
    # For Ultralytics YOLO, it's often easiest to pass a path for prediction
    temp_predict_path = "temp_for_yolo.jpg" # Temporary file for YOLO processing
    cv2.imwrite(temp_predict_path, img_bgr)
    results = model.predict(source=temp_predict_path, conf=conf_threshold, verbose=False)
    os.remove(temp_predict_path) # Clean up immediately
    inference_time = (time.time() - start_time) * 1000

    annotated_img = img_bgr.copy()
    detections = []

    if results[0].boxes is not None:
        for idx, box in enumerate(results[0].boxes, start=1):
            cls_id = int(box.cls)
            confidence = float(box.conf)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_name = CLASS_NAMES[cls_id] if cls_id < len(CLASS_NAMES) else f"class_{cls_id}"

            # Cavity = red, Normal = green
            color = (0, 0, 255) if cls_id == 0 else (0, 255, 0)  # 0=cavity (red), 1=normal (green)

            # Draw rectangle
            cv2.rectangle(annotated_img, (x1, y1), (x2, y2), color, 2)

            # Draw object number
            cv2.putText(annotated_img, str(idx), (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Probabilities array: [cavity_prob, normal_prob]
            probs = [0.0, 0.0]
            if cls_id == 0:  # cavity
                probs[0] = confidence
            elif cls_id == 1:  # normal
                probs[1] = confidence

            detections.append({
                'object_id': idx,
                'class_id': cls_id,
                'class_name': class_name,
                'confidence': confidence,
                'bbox': [x1, y1, x2, y2],
                'probabilities': probs
            })

    return annotated_img, detections, inference_time, original_size


def save_predictions_to_file(detections, original_image_size, filename):
    """Annotation saving is disabled as requested"""
    return None


def save_annotated_image(img_bgr, filename):
    """Image saving is disabled as requested"""
    return None


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/api/predict', methods=['POST'])
def api_predict():
    print("Received prediction request")
    if 'image' not in request.files:
        print("No image in request files")
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        print("Empty filename")
        return jsonify({'error': 'No image selected'}), 400

    try:
        print(f"Processing image: {image_file.filename}")
        original_filename = os.path.splitext(image_file.filename)[0]
        
        # Read image data directly into memory
        image_data = image_file.read()

        conf_threshold = float(request.form.get('confidence', CONFIDENCE_THRESHOLD))
        print(f"Confidence threshold: {conf_threshold}")

        # Pass in-memory image data to prediction function
        annotated_img, detections, inference_time, original_size = predict_with_yolo(image_data, conf_threshold)
        print(f"Prediction completed: {len(detections)} detections")
        
        # Convert annotated image to base64 for frontend display
        _, buffer = cv2.imencode('.jpg', annotated_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        return jsonify({
            'detections': detections,
            'inference_time_ms': round(inference_time, 2),
            'num_detections': len(detections),
            'confidence_threshold': conf_threshold,
            'annotated_image': img_base64  # Send Base64 image
        })

    except Exception as e:
        import traceback
        traceback.print_exc() # Print full traceback for debugging
        return jsonify({'error': str(e)}), 500


@app.route('/api/classes', methods=['GET'])
def get_classes():
    return jsonify({
        'classes': CLASS_NAMES,
        'num_classes': len(CLASS_NAMES)
    })


if __name__ == '__main__':
    if model is None:
        print("⚠️ Warning: Model not loaded.")
    app.run(debug=True, host='0.0.0.0', port=5000)