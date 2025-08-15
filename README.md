# 🦷 YOLOv12 Tooth Cavity Detection Dashboard

A modern web application for real-time tooth cavity detection using the YOLOv12 deep learning model. This project provides a user-friendly interface to upload dental images and visualize cavity predictions with bounding boxes directly in the browser, without saving any files to disk.

## ✨ Features

*   **Real-time Prediction**: Upload an image and get instant cavity detection results.
*   **Bounding Box Visualization**: Predicted cavities and normal teeth are highlighted with color-coded bounding boxes (red for cavity, green for normal).
*   **Interactive Probability Plot**: Visualize confidence scores for detected objects in a horizontal bar chart.
*   **In-Memory Processing**: Images are processed directly in memory; no temporary or result files are saved to your disk, ensuring a clean workspace.
*   **Responsive Web Interface**: A clean and intuitive user interface built with Flask, HTML, CSS (Bootstrap), and JavaScript (Chart.js).

## 🚀 Technologies Used

*   **Backend**: Python (Flask)
    *   **YOLOv12**: Ultralytics library for deep learning object detection.
    *   **OpenCV (`cv2`)**: For image processing and drawing bounding boxes.
    *   **NumPy**: For numerical operations, especially image handling.
    *   **Base64**: For encoding/decoding image data for web transfer.
*   **Frontend**: HTML, CSS (Bootstrap), JavaScript (Chart.js)
    *   **Chart.js**: For interactive data visualization (probability plots).
*   **Model**: Pre-trained YOLOv12 model (`best.pt`).

## 📁 Project Structure

```
YOLOv12-Tooth-Cavity-Detection/
├── .git/                      # Git repository information
├── models/
│   └── best.pt                # Pre-trained YOLOv12 model
├── ui/
│   ├── static/
│   │   ├── scripts.js         # Frontend JavaScript logic
│   │   └── styles.css         # Frontend CSS styles
│   └── templates/
│       └── index.html         # Main web application template
├── .gitignore                 # Specifies intentionally untracked files (Python interpreter paths)
├── app.py                     # Flask backend application
├── requirements.txt           # Python dependencies
├── LICENSE                    # Project license (MIT License)
└── README.md                  # Project README file
```

## ⚙️ Setup and Installation

Follow these steps to set up and run the project locally:

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/YOLOv12-Tooth-Cavity-Detection.git
    cd YOLOv12-Tooth-Cavity-Detection
    ```

2.  **Create a Virtual Environment** (Recommended):
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment**:
    *   **Windows**:
        ```bash
        .\venv\Scripts\activate
        ```
    *   **macOS/Linux**:
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note*: Ensure your system has CUDA drivers installed if you plan to use a GPU for faster inference with Ultralytics YOLO.

5.  **Place Your Model**:
    Make sure your `best.pt` YOLOv12 model file is placed in the `models/` directory.

## 🚀 Usage

1.  **Run the Flask Application**:
    ```bash
    python app.py
    ```
    The application will start, typically running on `http://127.0.0.1:5000/` or `http://localhost:5000/`.

2.  **Access the Dashboard**:
    Open your web browser and navigate to `http://localhost:5000/`.

3.  **Upload and Predict**:
    *   Click "Upload Image" to select a dental image (e.g., from the `samples images/` folder). You will see a preview of your uploaded image.
    *   Adjust the "Confidence Threshold" using the slider if needed.
    *   Click the "Predict" button.
    *   The "Uploaded Image" section will immediately update to show the image with detected bounding boxes (red for cavity, green for normal).
    *   The "Prediction Probabilities" chart will display confidence scores for each detected object.

## 🤝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 📧 Contact

For any questions or inquiries, please open an issue on the GitHub repository.

---
Enjoy using the YOLOv12 Tooth Cavity Detection Dashboard!