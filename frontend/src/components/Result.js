import React, { useEffect } from "react";
import "./Result.css";

const Result = ({ prediction, isLoading, error, image }) => {
  useEffect(() => {
    if (image) {
      console.log("Saving image to upload folder:", image);
    }
  }, [image]);

  return (
    <div className="result-container">
      {isLoading && <p className="loading">Loading...</p>}
      {error && <p className="error">{error}</p>}
      {prediction && <h2 className="result-prediction">Prediction: {prediction}</h2>}
    </div>
  );
};

export default Result;
