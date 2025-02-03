# Fault Detection & Quality Inspection System

🚀 **Project Overview**  
This project is a fully functional Fault Detection & Quality Inspection nd remote monitoring System that uses CNN Customize model without Using any Pre-trained Model with over 7000+ defected and non defected casting product images in warehouse and logistics with max 93% accuracy for defect detection and integrates with a Flask backend to serve predictions via a web interface. The frontend is built with HTML, CSS, and JavaScript to provide an intuitive and professional UI for:
- Uploading images or videos for defect detection with and can download csv file,total inpsection(with defected or non defected) see by visulise chart
- Live monitoring using a webcam and frame image can be see and download csv file of each product info which are showing live on UI.
- Storing and retrieving results seprate folder for image,video and live monitoring for image and csv
- Providing a clean, responsive UI with real-time feedback

This system can be used for industrial quality inspection in manufacturing, assembly lines, and defect analysis processes.

🚀 **Example**
A manufacturing company which do inspect daily 1000 casting product whatever they are defected or not. let's see how does time it will take inspection by manaully human VS this system if this will be implemented in that compnay.
- Human takes 10 seconds to inspect one product so it will take 1000 product*10 seconds by human which mean he will take apporx apporx = 2.77 hours rougly around 3 hours because human inspection typye is not uniform.
- let's say there if there is one conveyor belt and it takes 1 second to reach product 1 to the place of product 2, then we can set the web camara or other high quality camare on convery and when camara will start it will capurtes 30th(1 sec) of frame of the prouct which is passing throgh converyor belt and show the live data on UI and we can see the defected product by red boundry box and non defected by green boundry box on UI and all the caputured images and images information will be stored to data base which, we can see whenever we want on UI by filteration by day/week/total inpsected/ defected vs non defected and can download in csv format. and if it take 1 second to inspect one product then 1000 product*one sec = 16 min approx and if it inspect in two sec then it will take 32 min which is 18X(by 1 sec inspection) times or 9x(by 2 sec inspection) times faster than human inspection with store all data into strucuted format which human cant do. so this is the feature of this and additionally what we can do is we can also set a system that if model detect , faulty then it will push that to another conveyor and keep as it for non faulty so it can helpful.
-future scope 1. it take time nd affort to check that which part of big machines(where human cant see or can not identify that which part is in danger so for this we can use this same system though drone camara. 2. can be used to check high voltage current transformenrs at very high hight just to check qulity and if we human can do this manually so there are are chanlleges like we can fall fron electricity tower, death by minor errror when doing inspection with high current dangeer zone so we can use drone sysmtem here with same system of this model.

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