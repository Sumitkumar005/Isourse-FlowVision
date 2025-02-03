// resonsible for uploading manualy video which can will save into database and caputure every 60th frame(2 sec) of video and send that to model to check whatever it is faulty or not then it save their response as csv file and save every image which is in video with bounrdy box. and from this csv we can show the data such as history,total inspected product in that video, by diagram, and can download csv file from UI.
import React from "react";

const VideoResults = ({ videoUrl, metadata }) => {
  return (
    <div style={{ textAlign: 'center', margin: '20px' }}>
      <h3>Processed Video:</h3>
      <video width="600" controls>
        <source src={videoUrl} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <h4>Frame Metadata:</h4>
      <table style={{ margin: '20px auto', border: '1px solid black' }}>
        <thead>
          <tr>
            <th>Frame Number</th>
            <th>Filename</th>
            <th>Result</th>
          </tr>
        </thead>
        <tbody>
          {metadata.map((data, index) => (
            <tr key={index}>
              <td>{data.frame}</td>
              <td>{data.filename}</td>
              <td>{data.result}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default VideoResults;
