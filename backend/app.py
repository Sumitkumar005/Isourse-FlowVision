from flask import Flask, request, jsonify, send_from_directory
from flask import Flask, Response
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from werkzeug.utils import secure_filename
import os
from PIL import Image
import cv2
from datetime import datetime, timedelta  # Import datetime for timestamp
import threading
import time  # Import time for timestamping
from flask import Response



app = Flask(__name__)
CORS(app) 


@app.route("/")
def home():
    return "Flask backend is running!" 

# Load Model
model = tf.keras.models.load_model(r"E:\11111\New folder\final\react\backend\model\defect_detector_model.h5")
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((150, 150))  # Resize for model
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

def draw_bounding_box(image_path, result):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    color = (0, 0, 255) if result == "Defective" else (0, 255, 0)
    cv2.rectangle(image, (50, 50), (width - 50, height - 50), color, 4)
    # Save the image with the bounding box
    cv2.imwrite(image_path, image)

product_id_counter = 1  # Initialize product ID counter

@app.route("/predict", methods=["POST"])
def predict():
    global product_id_counter  # Declare the counter as global

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    img_array = preprocess_image(file_path)
    prediction = model.predict(img_array)[0][0]  # Assuming binary classification

    result = "Defective" if prediction < 0.5 else "Non-Defective"
    draw_bounding_box(file_path, result)  # Draw bounding box on the image
    # Save image data to CSV with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
    with open('image_data.csv', 'a') as f:
        f.write(f"{product_id_counter},{filename},{result},{timestamp}\n")
    
    product_id_counter += 1  # Increment the product ID counter

    return jsonify({"prediction": result, "image_url": f"/uploads/{filename}"})  # Return image URL

# New endpoint to handle webcam streaming and defect detection
@app.route("/webcam", methods=["POST"])
def webcam():
    global product_id_counter
    live_monitoring_folder = "live_monitoring"
    os.makedirs(os.path.join(os.path.dirname(__file__), live_monitoring_folder), exist_ok=True)

    cap = cv2.VideoCapture(0)  # Start the webcam
    if not cap.isOpened():
        return jsonify({"error": "Could not open webcam"}), 500

    predictions = []
    frame_num = 0
    frame_interval = 60  # Analyze every 60th frame
    max_predictions = 15  # Limit to 15 predictions

    # Get the width and height of the video stream
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while cap.isOpened() and len(predictions) < max_predictions:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        frame_num += 1

        if frame_num % frame_interval != 0:
            continue  # Skip frames

        # Convert the frame (BGR format) to RGB and then to a PIL Image
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame_rgb)

        # Resize and normalize the image (matching your model's expected input)
        pil_img = pil_img.resize((150, 150))
        img_array = np.array(pil_img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict using your model
        prediction = model.predict(img_array)[0][0]
        result = "Defective" if prediction < 0.5 else "Non-Defective"

        # Draw bounding box
        color = (0, 0, 255) if result == "Defective" else (0, 255, 0)
        cv2.rectangle(frame, (50, 50), (width - 50, height - 50), color, 4)

        # Save the frame with bounding box
        timestamp = int(time.time())
        output_frame_path = os.path.join(live_monitoring_folder, f"product_{product_id_counter}.jpg")
        cv2.imwrite(output_frame_path, frame)

        predictions.append({"frame": frame_num, "result": result})

    cap.release()
    return jsonify({"message": "Webcam processing completed", "predictions": predictions})


# New endpoint to serve uploaded images
@app.route('/uploads/<path:filename>', methods=['GET'])
def get_uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# New endpoint to download the CSV file
@app.route('/download_csv', methods=['GET'])
def download_csv():
    return send_from_directory(os.getcwd(), 'image_data.csv', as_attachment=True)

# New endpoint to get recent uploaded images and their predictions
@app.route("/uploaded_images", methods=["GET"])
def uploaded_images():
    images = os.listdir(app.config["UPLOAD_FOLDER"])
    images.sort(key=lambda x: os.path.getmtime(os.path.join(app.config["UPLOAD_FOLDER"], x)), reverse=True)  # Sort by modification time
    recent_images = images[:5]  # Get the last 5 uploaded images

    predictions = []
    for image in recent_images:
        img_array = preprocess_image(os.path.join(app.config["UPLOAD_FOLDER"], image))
        prediction = model.predict(img_array)[0][0]  # Assuming binary classification
        result = "Defective" if prediction < 0.5 else "Non-Defective"
        predictions.append({"filename": image, "result": result})

    return jsonify(predictions)

# New endpoint to get inspection data
@app.route("/inspections", methods=["GET"])
def inspections():
    time_range = request.args.get("range", "today")  # Default to today
    today = datetime.now().date()
    start_date = None
    end_date = None

    if time_range == "today":
        start_date = today
        end_date = today
    elif time_range == "yesterday":
        start_date = today - timedelta(days=1)
        end_date = today - timedelta(days=1)
    elif time_range == "last_7_days":
        start_date = today - timedelta(days=7)
        end_date = today
    elif time_range == "last_30_days":
        start_date = today - timedelta(days=30)
        end_date = today

    defective_count = 0
    non_defective_count = 0

    with open('image_data.csv', 'r') as f:
        for line in f:
            line_data = line.strip().split(',')
            if len(line_data) != 4:  # Ensure there are exactly 4 values
                continue  # Skip this line if it doesn't have the correct format
            product_id, filename, result, timestamp = line_data

            timestamp_date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").date()
            if start_date <= timestamp_date <= end_date:
                if result == "Defective":
                    defective_count += 1
                else:
                    non_defective_count += 1

    return jsonify({
        "defective": defective_count,
        "non_defective": non_defective_count,
        "total": defective_count + non_defective_count
    })

# New endpoint to upload and process video
@app.route("/upload_video", methods=["POST"])
def upload_video():
    global product_id_counter
    if "file" not in request.files:
        return jsonify({"error": "No video file uploaded"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Process video frames using OpenCV
    cap = cv2.VideoCapture(file_path)
    predictions = []
    frame_num = 0
    frame_interval = 30  # Process every 30th frame
    max_predictions = 10  # Limit to 10 predictions

    output_video_path = os.path.join(app.config["UPLOAD_FOLDER"], "processed_" + filename)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = cap.get(cv2.CAP_PROP_FPS) / frame_interval  # Adjust FPS for output
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    while cap.isOpened() and len(predictions) < max_predictions:
        ret, frame = cap.read()
        if not ret:
            break
        frame_num += 1

        if frame_num % frame_interval != 0:
            continue  # Skip frames

        # Convert the frame (BGR format) to RGB and then to a PIL Image
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame_rgb)

        # Resize and normalize the image (matching your model's expected input)
        pil_img = pil_img.resize((150, 150))
        img_array = np.array(pil_img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict using your model
        prediction = model.predict(img_array)[0][0]
        result = "Defective" if prediction < 0.5 else "Non-Defective"

        # Draw bounding box
        color = (0, 0, 255) if result == "Defective" else (0, 255, 0)
        cv2.rectangle(frame, (50, 50), (width - 50, height - 50), color, 4)

        predictions.append({"frame": frame_num, "result": result})

        out.write(frame)  # Save processed frame

    cap.release()
    out.release()

    return jsonify({"message": "Video processed successfully", "video_url": f"/uploads/processed_{filename}", "predictions": predictions}


# New generator function to stream webcam frames with defect detection annotation
def gen_live_frames():
    cap = cv2.VideoCapture(0)  # Open default webcam
    if not cap.isOpened():
        raise RuntimeError("Could not start webcam.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Get frame dimensions
        height, width, _ = frame.shape

        # --- Process frame using your model ---
        # Convert frame (BGR) to RGB, resize, and preprocess
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame_rgb)
        pil_img = pil_img.resize((150, 150))
        img_array = np.array(pil_img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict using your defect detection model
        prediction = model.predict(img_array)[0][0]
        result = "Defective" if prediction < 0.5 else "Non-Defective"

        # Draw bounding box and label on the original frame
        color = (0, 0, 255) if result == "Defective" else (0, 255, 0)
        cv2.rectangle(frame, (50, 50), (width - 50, height - 50), color, 4)
        cv2.putText(frame, result, (60, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        # --- End processing ---

        # Encode the frame in JPEG format
        ret2, buffer = cv2.imencode('.jpg', frame)
        if not ret2:
            continue
        frame_bytes = buffer.tobytes()

        # Yield the frame in a multipart response format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.03)  # Adjust sleep to control stream FPS

    cap.release()

# New endpoint for live webcam streaming
@app.route('/live_video_stream')
def live_video_stream():
    return Response(gen_live_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
