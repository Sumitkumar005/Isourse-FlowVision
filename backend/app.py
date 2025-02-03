from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import pandas as pd
from flask import Flask, jsonify, request
import numpy as np
from werkzeug.utils import secure_filename
import os
from PIL import Image
import cv2
from datetime import datetime, timedelta 
import csv
import time 

app = Flask(__name__)
CORS(app) 

@app.route("/")
def home():
    return "Flask backend is running!" #just to check that our bakend working or not

#1 Load Model
model = tf.keras.models.load_model(r"E:\11111\react\backend\model\defect_detector_model.h5") #it have 85% accurucy 
UPLOAD_FOLDER = "uploads" #this stores only inspected images
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((150, 150))  # can resize the image accordingly to model capicity
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

WEBCAM_IMAGE_FOLDER = "webcam_image_folder" #stored live inspected monitoring images  which firstly live cam caputure 60th frame(2 sec) and saving those image into this folder so we can see the image if we want from video with boundybox
os.makedirs(WEBCAM_IMAGE_FOLDER, exist_ok=True)


CSV_FILE_PATH = "webcam.csv" # stored inspected image infomation with sr no., image name, result, time and data and responsibel for sending this information to UI, where this data will be used to  show as diagram, total inspection history 
df = pd.read_csv("webcam.csv")
if not os.path.exists(CSV_FILE_PATH):
    with open(CSV_FILE_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Frame Number", "Result", "Image Path"])


def draw_bounding_box(image_path, result): #boundry box around the product when it pass throuh ml model as defected or not.
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    color = (0, 0, 255) if result == "Defective" else (0, 255, 0)
    cv2.rectangle(image, (50, 50), (width - 50, height - 50), color, 4)
    cv2.imwrite(image_path, image)

product_id_counter = 1 

@app.route("/predict", methods=["POST"]) #main endpoint to which delcalre that image defected or not, and used for all when we upload image, video, and live web cam monitoring  and check whatever it falut or not then give response back to them.
def predict():
    global product_id_counter 

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    img_array = preprocess_image(file_path)
    prediction = model.predict(img_array)[0][0] 

    result = "Defective" if prediction < 0.5 else "Non-Defective" # if we have more than two classed we can use module somthing for that.
    draw_bounding_box(file_path, result) 
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    with open('image_data.csv', 'a') as f:
        f.write(f"{product_id_counter},{filename},{result},{timestamp}\n")
    
    product_id_counter += 1  # Increment the product ID counter

    return jsonify({"prediction": result, "image_url": f"/uploads/{filename}"}) 


# endpoint to serve uploaded images
@app.route('/uploads/<path:filename>', methods=['GET'])
def get_uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# endpoint to download the CSV file
@app.route('/download_csv', methods=['GET'])
def download_csv():
    return send_from_directory(os.getcwd(), 'image_data.csv', as_attachment=True)

# endpoint to get recent uploaded images and their predictions
@app.route("/uploaded_images", methods=["GET"])
def uploaded_images():
    images = os.listdir(app.config["UPLOAD_FOLDER"])
    images.sort(key=lambda x: os.path.getmtime(os.path.join(app.config["UPLOAD_FOLDER"], x)), reverse=True)  
    recent_images = images[:5]  # Get the last 5 uploaded images

    predictions = []
    for image in recent_images:
        img_array = preprocess_image(os.path.join(app.config["UPLOAD_FOLDER"], image))
        prediction = model.predict(img_array)[0][0] 
        result = "Defective" if prediction < 0.5 else "Non-Defective"
        predictions.append({"filename": image, "result": result})

    return jsonify(predictions)

#endpoint to get inspection data
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
            if len(line_data) != 4:
                continue  
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

# endpoint to upload and process video
@app.route("/upload_video", methods=["POST"])
def upload_video():
    global product_id_counter
    if "file" not in request.files:
        return jsonify({"error": "No video file uploaded"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Process video frames using OpenCV and save every 60th frame as an image
    os.makedirs("video_processing_images", exist_ok=True)  # directory for images
    metadata = []  

    cap = cv2.VideoCapture(file_path)
    predictions = []
    frame_num = 0
    frame_interval = 30  # Process every 30th frame
    max_predictions = 10  # Limit to 10 predictions

    output_video_path = os.path.join(app.config["UPLOAD_FOLDER"], "processed_" + filename)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = cap.get(cv2.CAP_PROP_FPS) / frame_interval 
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    while cap.isOpened() and len(predictions) < max_predictions:
        ret, frame = cap.read()
        if not ret:
            break
        frame_num += 1

        if frame_num % frame_interval != 0:
            continue  

        # Convert the frame (BGR format) to RGB and then to a PIL Image
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame_rgb)

        # Resize and normalize the image (matching model's expected input)
        pil_img = pil_img.resize((150, 150))
        img_array = np.array(pil_img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict using model
        prediction = model.predict(img_array)[0][0]
        result = "Defective" if prediction < 0.5 else "Non-Defective"

        # Draw bounding box
        color = (0, 0, 255) if result == "Defective" else (0, 255, 0)
        cv2.rectangle(frame, (50, 50), (width - 50, height - 50), color, 4)

        # Save the frame as an image every 60th frame
        if frame_num % frame_interval == 0:
            image_filename = f"video_processing_images/frame_{frame_num}.jpg"
            cv2.imwrite(image_filename, frame)  # Save the frame as an image
            metadata.append({"frame": frame_num, "filename": image_filename, "result": result})  # Store metadata


        out.write(frame)

    cap.release()
    out.release()

    # Save data to CSV
    with open('video_metadata.csv', 'a') as f:
        for data in metadata:
            f.write(f"{data['frame']},{data['filename']},{data['result']}\n")

    return jsonify({
        "message": "Video processed successfully",
        "video_url": f"/uploads/processed_{filename}",
        "predictions": predictions,
        "metadata": metadata
    })


@app.route("/webcam", methods=["POST"]) #main for live monitoring but it not showing live cam result on UI when cam start coz of gpu but logic and code are correct. but i have added a video to live monitoring folder in backend folder you can checkout there. and webcam folder for live cam image caputure which stored there with reuslt and time and checkout webcam.csv file which stored live image information when live monitoring start to end. and this csv file data retrive to UI to show the live cam monitoring informtion through diagram,total inspected while live monitoring,defected and non defected, detection logs, history.
def webcam():
    cap = cv2.VideoCapture(0)  # Start the live web cam
    frame_count = 0
    results = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % 60 == 0:  # Process every 60th frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resized_frame = cv2.resize(frame_rgb, (150, 150))
            img_array = np.array(resized_frame) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            prediction = model.predict(img_array)[0][0]
            result = "Defective" if prediction < 0.85 else "Non-Defective"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            img_path = os.path.join(WEBCAM_IMAGE_FOLDER, f"frame_{frame_count}.jpg")

            cv2.imwrite(img_path, frame)

            # Draw bounding box on the frame
            cv2.rectangle(frame, (50, 50), (250, 250), (0, 255, 0), 2)
            cv2.putText(frame, result, (60, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            with open(CSV_FILE_PATH, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([frame_count, result, img_path, timestamp])
                
            results.append({"frame": frame_count, "result": result})

           
        cv2.imshow("Live Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    return jsonify({"message": "Webcam processing completed", "predictions": results})    
#histroy endpoint for to show UI
@app.route("/history", methods=["GET"])
def history():
    filter_type = request.args.get("filter", "today")
    df = pd.read_csv(CSV_FILE_PATH)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    today = datetime.now().date()
    
    if filter_type == "today":
        df = df[df["Timestamp"].dt.date == today]
    elif filter_type == "yesterday":
        df = df[df["Timestamp"].dt.date == today - pd.Timedelta(days=1)]
    elif filter_type == "weekly":
        df = df[df["Timestamp"] >= today - pd.Timedelta(weeks=1)]
    elif filter_type == "monthly":
        df = df[df["Timestamp"] >= today - pd.Timedelta(days=30)]
    
    return jsonify(df.to_dict(orient="records"))  
             
#live info of monitoring on UI
@app.route('/live_data')
def live_data():
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        total_inspected = len(df)
        defective = df[df['Result'] == 'Defective'].shape[0]
        non_defective = df[df['Result'] == 'Non-Defective'].shape[0]

        return jsonify({
            "total_inspected": total_inspected,
            "defective": defective,
            "non_defective": non_defective
        })
    except Exception as e:
        return jsonify({"error": str(e)})

    
if __name__ == "__main__":
    app.run(debug=True)
