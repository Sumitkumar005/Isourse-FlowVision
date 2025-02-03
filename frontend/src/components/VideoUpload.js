// resonsible for uploading manualy video which can will save into database and caputure every 60th frame(2 sec) of video and send that to model to check whatever it is faulty or not then it save their response as csv file and save every image which is in video with bounrdy box. and from this csv we can show the data such as history,total inspected product in that video, by diagram, and can download csv file from UI.

import React, { useState } from "react";
import axios from "axios";

const VideoUpload = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [videoUrl, setVideoUrl] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage(""); // Reset message on file change
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a video file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setMessage(""); // Reset message before upload

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload_video", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setVideoUrl(`http://127.0.0.1:5000${response.data.video_url}`); // Set video URL for playback
      setMessage("Video processed successfully!"); // Success message
    } catch (error) {
      console.error("Error uploading video:", error);
      setMessage("Error uploading video. Please try again."); // Error message
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: 'center', margin: '20px' }}>
      <input type="file" onChange={handleFileChange} accept="video/*" />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Uploading..." : "Upload Video"}
      </button>
      {message && <p>{message}</p>} {/* Display success/error message */}
      {videoUrl && (
        <div>
          <h3>Processed Video:</h3>
          <video width="600" controls>
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
    </div>
  );
};

export default VideoUpload;
