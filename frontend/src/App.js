import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import Result from "./components/Result";
import LiveWebcam from "./components/LiveWebcam";
import Header from "./components/Header"; // Import Header
import Footer from "./components/Footer"; // Import Footer
import "./App.css";

function App() {
  const [prediction, setPrediction] = useState("");

  return (
    <div className="container">
      <Header /> {/* Render Header */}
      <h1>Defect Detection System</h1>
      <UploadForm setPrediction={setPrediction} />
      <Result prediction={prediction} />
      <LiveWebcam />

      <Footer /> {/* Render Footer */}
    </div>
  );
}

export default App;
