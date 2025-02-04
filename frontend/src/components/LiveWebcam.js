// LiveWebcam.js
import React from "react";

const LiveWebcam = () => {
  // Adjust the URL if your backend is hosted elsewhere
  const streamUrl = "http://127.0.0.1:5000/live_video_stream";

  return (
    <div style={{ textAlign: "center", margin: "20px" }}>
      <h3>Live Webcam Feed</h3>
      <img
        src={streamUrl}
        alt="Live Webcam Feed"
        style={{ width: "600px", border: "1px solid #ccc" }}
      />
      <p>
        If the stream doesn't load, please ensure your backend is running and accessible.
      </p>
    </div>
  );
};

export default LiveWebcam;
