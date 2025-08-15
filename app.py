from flask import Flask, render_template, request, jsonify, send_file
from ultralytics import YOLO
import cv2
import os
import time
from datetime import datetime

app = Flask(__name__)

# === CONFIGURATION ===
MODEL_PATH = 'models/best.pt'  # Path to your YOLO model
CONFIDENCE_THRESHOLD = 0.25
UPLOAD_FOLDER = 'temp_uploads'
RESULTS_FOLDER = 'results'
ANNOTATIONS_FOLDER = 'annotations'

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(ANNOTATIONS_FOLDER, exist_ok=True)

# === CLASSES (modify for your dataset) ===
CLASS_NAMES = ['cavity', 'normal']  # index 0 = cavity, index 1 = normal


# === Load YOLO model ===
try:
    model = YOLO(MODEL_PATH)
    print(f"✅ Model loaded from {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None


def predict_with_yolo(image_path, conf_threshold=0.25):
    """
    Run YOLO prediction and return annotated image + detection data
    """
    if model is None:
        raise Exception("Model not loaded")

    img_bgr = cv2.imread(str(image_path))
    if img_bgr is None:
        raise Exception("Could not load image")

    original_size = (img_bgr.shape[1], img_bgr.shape[0])

    # YOLO prediction
    start_time = time.time()
    results = model.predict(source=str(image_path), conf=conf_threshold, verbose=False)
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
    """Save predictions in YOLO text format"""
    width, height = original_image_size
    annotation_file = os.path.join(ANNOTATIONS_FOLDER, f"{filename}.txt")

    with open(annotation_file, 'w') as f:
        for detection in detections:
            cls_id = detection['class_id']
            x1, y1, x2, y2 = detection['bbox']

            center_x = ((x1 + x2) / 2) / width
            center_y = ((y1 + y2) / 2) / height
            bbox_width = (x2 - x1) / width
            bbox_height = (y2 - y1) / height

            f.write(f"{cls_id} {center_x:.6f} {center_y:.6f} {bbox_width:.6f} {bbox_height:.6f} {detection['confidence']:.6f}\n")

    return annotation_file


def save_annotated_image(img_bgr, filename):
    """Save annotated image to results folder"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_filename = f"{filename}_{timestamp}_predicted.jpg"
    result_path = os.path.join(RESULTS_FOLDER, result_filename)
    cv2.imwrite(result_path, img_bgr)
    return result_path


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
        temp_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
        image_file.save(temp_path)
        print(f"Image saved to: {temp_path}")

        conf_threshold = float(request.form.get('confidence', CONFIDENCE_THRESHOLD))
        print(f"Confidence threshold: {conf_threshold}")

        annotated_img, detections, inference_time, original_size = predict_with_yolo(temp_path, conf_threshold)
        print(f"Prediction completed: {len(detections)} detections")
        saved_image_path = save_annotated_image(annotated_img, original_filename)
        annotation_file_path = save_predictions_to_file(detections, original_size, original_filename)

        os.remove(temp_path)

        return jsonify({
            'detections': detections,
            'inference_time_ms': round(inference_time, 2),
            'num_detections': len(detections),
            'confidence_threshold': conf_threshold,
            'saved_image_path': os.path.basename(saved_image_path),
            'annotation_file_path': os.path.basename(annotation_file_path)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/image/<filename>')
def download_image(filename):
    file_path = os.path.join(RESULTS_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=False)
    return jsonify({'error': 'File not found'}), 404


@app.route('/download/annotation/<filename>')
def download_annotation(filename):
    file_path = os.path.join(ANNOTATIONS_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, mimetype='text/plain')
    return jsonify({'error': 'File not found'}), 404


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
