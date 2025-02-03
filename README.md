# Fault Detection & Quality Inspection System

🚀 **Project Overview**  
This project is a fully functional Fault Detection and Quality Inspection System with remote monitoring capabilities. It uses a custom CNN model (without relying on any pre-trained models) to detect defects in casting products. The system has been trained on over 7,000 defected and non-defected product images ([Download Dataset](https://drive.google.com/file/d/1shOZ30VLqwoPIH9LC_dxPZ53TjpC_ZP9/view?usp=sharing)) from warehouse and logistics environments, achieving a maximum accuracy of 93% for defect detection. The project integrates a Flask backend to serve predictions through a web interface, while the frontend is built using HTML, CSS, and JavaScript to provide an intuitive and professional user interface.
- Upload Images or Videos: Users can upload images or videos for defect detection and receive predictions. Results can be downloaded as a CSV file, showing total inspections with either defected or non-defected products.
- Live Monitoring: Live monitoring using a webcam to capture frames. The image of each product is displayed, and a CSV file of each product’s information (such as defect status) is downloadable directly from the UI.
- Storage and Retrieval: Results are stored in separate folders for images, videos, and live monitoring. Each folder contains relevant images/videos and corresponding CSV files.
-Real-Time Feedback: The UI provides real-time feedback to users with a clean, responsive layout, enabling seamless interactions.

This system can be used for industrial quality inspection in manufacturing, assembly lines, and defect analysis processes.

🚀 **Example**

A manufacturing company inspects 1000 casting products daily, whether they are defected or not. Let’s compare how much time it would take to inspect manually by humans versus using this system if implemented in that company.
- A human takes 10 seconds to inspect one product. So, for 1000 products, it would take 1000 * 10 seconds, which means approximately 2.77 hours, roughly around 3 hours, because human inspection time is not uniform.
- Now, let’s say there is a conveyor belt where it takes 1 second for one product to reach the next position. We can place a webcam or another high-quality camera on the conveyor belt, and when the camera starts, it will capture a frame every 1 second of the product passing through. The live data will be shown on the UI, and defected products will have a red boundary box, while non-defected products will have a green boundary box. All captured images and their corresponding information will be stored in the database, and we can view the data anytime on the UI, filter by day/week/total inspected, defected vs non-defected, and download the data in CSV format.
- If it takes 1 second to inspect one product, 1000 products * 1 second = approximately 16 minutes. If it takes 2 seconds per product, it will take about 32 minutes. This makes the system 18x (with 1 second inspection) or 9x (with 2 seconds inspection) faster than human inspection, while also storing all the data in a structured format, which humans can’t do

This is one of the features of the system. Additionally, we can set up a system where, if the model detects a faulty product, it will push it to another conveyor for separate handling, keeping the non-faulty products safe.
  
**future scope**
- 1.It takes time and effort to inspect parts of large machines that humans can’t see or identify as potentially dangerous. We can use the same system with drone cameras for this purpose.
- 2.The system can also be used to inspect high-voltage transformers located at very high altitudes. This is critical because inspecting such equipment manually comes with many challenges. Humans could fall from electricity towers or even die due to minor errors when working in high-voltage danger zones. The drone system, using this model, could greatly improve safety and efficiency in such high-risk inspections.

________________________________________

📌 **Key Features**
- 🔍 Defect Detection: Upload an image or video and receive a defect classification with a confidence score.
- 📷 Live Monitoring: Use a webcam for real-time fault detection.
- 💾 Storage System: Automatically stores processed images/videos for future reference.
- 🖥 Professional UI/UX: Built using Bootstrap & JavaScript for a smooth user experience.

________________________________________

🛠️ **Technologies Used**
- Machine Learning: CNN, Keras
- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript,
- Data Handling: OpenCV, NumPy, Pandas
- Storage & File Handling: Google Drive / Local Directory
- Live Streaming: OpenCV

________________________________________

📂 **Project Folder Structure**
```
fault-detection-dashboard/
│── backend/                   # Flask Backend (API & ML Model)
│   ├── model/                 # YOLO Custom Model Files
│   ├── uploads/               # dectected manually uploaded images
│   ├── live_monitoring/       # Live Monitoring video(database)
│   ├── app.py                 # Main API (Flask)
│   ├── video_processing_images# Extracted frames images from video(defected or not)
│   ├── webcam_image_folder    # Extracted frames images from Live Monitoring video(defected or not)
│   ├── image_data.csv         # stored info of uploaded images (used to retrive information on UI)
│   ├── video_metadata.csv     # stored info of uploaded videos (used to retrive information on UI)
│   ├── webcam.csv             # stored info of live monitoring videos (used to retrive on UI)
│   ├── requirements.txt       # Dependencies
│   ├── config.py              # Configuration variables
│
│── frontend/                  # React.js + CSS
│   ├── public/  
│   │   ├──index.html          # basic
│   ├── src/                   # Main source
│   │   ├── components/        # Reusable components
│   │   │   ├── App.css
│   │   │   ├── footer.js
│   │   │   ├── Header.js
│   │   │   ├── livewevcammonitoring.js #for live monitoring
│   │   │   ├── Result.js
│   │   │   ├── Result.css
│   │   │   ├── UploadForm.js  #for image uploading
│   │   │   ├── VideoResult.js  
│   │   │   ├── VideoUpload.js #for video uploading
│   │   │   ├── HistoryTable.js
│   │   ├── App.js             # Main frontend app
│   │   ├── App.css
│   │   ├── index.js           # React entry point
│   │   ├── index.css
│   ├── package.json           # Dependencies
│   ├── package-lock.json
│
│── README.md                  # Complete Documentation
│── .gitignore                  # Ignore files like `__pycache__`
│── current basic ui demo.mp4   # demo
│── current basic ui.jpg        #basic ui
│── current basic ui.mp4        #real UI
```

________________________________________

🔥 **Key Features & Components**
1️⃣ **User Authentication (Login/Logout)**
- Secure API calls
- Stores login logs

2️⃣ **Dashboard (Main Interface After Login)**
- ✅ Live Monitoring (Webcam)
- ✅ File Upload (Images & Videos for Inspection)
- ✅ Detection Results (Displays def_front or ok_front)
- ✅ Real-Time Fault Visualization (Chart.js)
- ✅ Recent 5 Inspections (Table showing last 5 uploads)
- ✅ Historical Data Export (Download CSV of past inspections)
- ✅ Toggle ON/OFF Live Webcam Monitoring
- ✅ System Logs (Errors, Events, API Calls, User Actions)

________________________________________

📊 **Dashboard Components (Professional UI/UX)**
1️⃣ Navigation Bar (Home | Upload | History | Live)
2️⃣ Live Stream Section (Start/Stop Webcam)
3️⃣ Upload Image/Video (Button with drag-drop feature)
4️⃣ Detection Results (Confidence Score, Detected Label)
5️⃣ Fault Trends (Bar Chart & Pie Chart)
6️⃣ Recent Inspections Table (Last 5 Inspected Images with Timestamp)
7️⃣ Export CSV Button (Download inspection history)
8️⃣ Toggle Live Monitoring (ON/OFF for Remote Monitoring)
9️⃣ System Logs Panel (Real-time activity tracking)

________________________________________

🛠️ **Additional Enhancements can be for improvements**
- ✔ Professional UI (Material-UI / TailwindCSS for Modern Look)
- ✔ WebSocket for Real-Time Communication (Flask-SocketIO)
- ✔ Dockerized Deployment (Easy Server Setup)
- ✔ Cloud Storage Support (AWS S3 for Storing Media Files)
- ✔ Logging System (User actions, API calls, error handling)

________________________________________

📌 **Installation & Setup**
Follow these steps to set up the project from scratch.

**Step 1: Clone the Repository**
```bash
git clone https://github.com/yourusername/fault-detection-system.git
cd fault-detection-system
```

**Step 2: Create a Virtual Environment & Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
pip install -r requirements.txt
```

**Step 3: Set Up Google Drive for Dataset (Optional)**
If using Google Drive for dataset storage:
1. Mount Google Drive in Colab: 
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
2. Ensure datasets and models are stored under `/content/drive/MyDrive/your_project/`

**Step 4: Download & Train CNN**
```bash
model.train(data="dataset.yaml", epochs=50, imgsz=640)
model.export(format=".h") 
```

________________________________________

🎯 **Flask Backend Implementation**
The Flask server handles file uploads, live monitoring, and defect detection API calls.

**Running the Flask Server**
```bash
python app.py
```

**API Endpoints**
| Endpoint   | Method | Description                                   |
|------------|--------|-----------------------------------------------|
| /upload    | POST   | Upload an image and return defect classification |
| /webcam    | GET    | Access live webcam monitoring                  |
| /results   | GET    | Retrieve past defect analysis                  |

________________________________________

🖥️ **Frontend (HTML, CSS, JavaScript)**
The frontend provides a modern UI with:
- File Upload System for images/videos
- Webcam Integration for live monitoring
- Dynamic Result Display with real-time updates

**Key UI Components**
- ✔ File Upload Section (Drag & Drop or Select File)
- ✔ Live Webcam Stream (Capture and Analyze)
- ✔ Prediction Results Panel

________________________________________

🎥 **Live Monitoring Setup (Webcam)**
To enable live monitoring, use OpenCV in the backend:
```python
import cv2
from flask import Response

@app.route('/webcam')
def webcam_feed():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    cap.release()
```

________________________________________

🏆 **Challenges Faced & Solutions**
1️⃣ **Model Performance Optimization**
   - ✅ Challenge: Initial model had low accuracy on defects.
   - ✅ Solution: incresed size of epoch, and fine-tuned hyperparameters.

2️⃣ **Flask API Response Time**
   - ✅ Challenge: Slow response time when processing large images.
   - ✅ Solution: Used ONNX format for faster inference.

3️⃣ **Frontend Integration with Flask**
   - ✅ Challenge: UI not updating predictions in real time.
   - ✅ Solution: Used JavaScript Fetch API to call Flask endpoints dynamically.

________________________________________

🚀 **Future Enhancements**
- 🔹 Add Support for Videos: Extend model to analyze full video streams.
- 🔹 Optimize UI/UX: Improve user interface with animations & better feedback mechanisms.
- 🔹 Deploy to Cloud: Deploy on AWS/GCP for scalable inference.
________________________________________

📜 **Conclusion**
If you find this project helpful, give it a star ⭐ and feel free to contribute by improving the model or UI. For any questions, open an issue or contact me at sumitkumar969074@gmail.com 🚀

This project took 15 days of rigorous work, including:
- ✔ Model training & tuning (Custom CNN)
- ✔ Backend development (Flask)
- ✔ Frontend integration (HTML, CSS, JavaScript)
- ✔ Real-time webcam monitoring

Every step was built from scratch, demonstrating expertise in computer vision, web development, and backend APIs. This repository serves as a blueprint for defect detection projects across industries.

________________________________________

⭐ **Contributer**
- Sumit Kumar
- Prasad Khare
