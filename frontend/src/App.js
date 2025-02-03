// main JS file which import all the components and responsible to show on UI.

import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import Result from "./components/Result";
import VideoUpload from "./components/VideoUpload"; 
import VideoResults from "./components/VideoResults"; 
import Header from "./components/Header"; 
import Footer from "./components/Footer"; 
import LiveWebcamMonitoring from "./components/livewevcammonitoring"; 
import "./App.css";

function App() {
  const [prediction, setPrediction] = useState("");
  const [videoUrl, setVideoUrl] = useState("");
  const [metadata, setMetadata] = useState([]);

  return (
    <div className="container">
      <Header /> {/* Render Header */}
      <h1>Defect Detection System</h1>
      <UploadForm setPrediction={setPrediction} />
      <VideoUpload setVideoUrl={setVideoUrl} setMetadata={setMetadata} /> {/* Render VideoUpload component */}
      <Result prediction={prediction} />
      {videoUrl && <VideoResults videoUrl={videoUrl} metadata={metadata} />} {/* Render VideoResults component if videoUrl is set */}
      <LiveWebcamMonitoring /> {/* Render LiveWebcamMonitoring component */}
      <Footer /> {/* Render Footer */}
    </div>
  );
}

export default App;
