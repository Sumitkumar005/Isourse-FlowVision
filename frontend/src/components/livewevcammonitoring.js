
// responsible for live monitoring of the system
import React, { useRef, useState, useEffect } from "react";
import axios from "axios";
import Chart from "chart.js/auto";

const LiveWebcamMonitoring = () => {
    const videoRef = useRef(null);
    const [isStreaming, setIsStreaming] = useState(false);
    const [logs, setLogs] = useState([]);
    const [defectCount, setDefectCount] = useState(0);
    const [totalInspected, setTotalInspected] = useState(0);
    const [nonDefectiveCount, setNonDefectiveCount] = useState(0);
    const [chartData, setChartData] = useState({ labels: [], data: [] });
    const [timeFilter, setTimeFilter] = useState("today");
    let chartInstance = null;

    useEffect(() => {
        if (isStreaming) {
            const fetchLiveData = () => {
                axios.get("http://127.0.0.1:5000/live_data") //fetch endpoint from Flask main app
                    .then(response => {
                        const { total, defective, non_defective } = response.data;
                        setTotalInspected(total);
                        setDefectCount(defective);
                        setNonDefectiveCount(non_defective);
                    })
                    .catch(error => console.error("Error fetching live data:", error));
            };
            const interval = setInterval(fetchLiveData, 2000);
            return () => clearInterval(interval);
        }
    }, [isStreaming]);

    const startWebcam = async () => {
        setIsStreaming(true);
        setLogs([]);
        setDefectCount(0);
        setTotalInspected(0);
        setNonDefectiveCount(0);

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            videoRef.current.srcObject = stream;
            await axios.post("http://127.0.0.1:5000/webcam"); // main for live monitoring 
        } catch (error) {
            console.error("Error starting webcam:", error);
        }
    };

    const stopWebcam = () => {
        setIsStreaming(false);
        if (videoRef.current.srcObject) {
            const stream = videoRef.current.srcObject;
            stream.getTracks().forEach(track => track.stop());
            videoRef.current.srcObject = null;
        }
    };
// history fuction not retriving(stored data into csv file and webcam image folder) nd showing live web cam monitoring informaiton on UI but Sir i can fix it later coz today is deadline!
    const fetchHistoryData = () => {
        axios.get(`http://127.0.0.1:5000/history?filter=${timeFilter}`) //retrived live camara monitoring  data as csv as show them on UI as diagram with day/weekly/monthly so we can track the information
            .then(response => {
                setChartData({ labels: response.data.labels, data: response.data.data });
                renderChart(response.data);
            })
            .catch(error => console.error("Error fetching history data:", error));
    };

    useEffect(() => {
        fetchHistoryData();
    }, [timeFilter]);

    const renderChart = (data) => {
        if (chartInstance) {
            chartInstance.destroy();
        }
        const ctx = document.getElementById("historyChart").getContext("2d");
        chartInstance = new Chart(ctx, {
            type: "bar",
            data: {
                labels: data.labels,
                datasets: [{
                    label: "Inspection Results",
                    data: data.data,
                    backgroundColor: ["#4caf50", "#f44336"],
                }]
            },
        });
    };

    return (
        <div className="webcam-container">
            <h2>Live Webcam Monitoring</h2>
            <video ref={videoRef} autoPlay className="webcam-video" />
            <div className="webcam-controls">
                <button onClick={startWebcam} disabled={isStreaming}>Start Webcam</button>
                <button onClick={stopWebcam} disabled={!isStreaming}>Stop Webcam</button>
            </div>
            <h3>Total Inspected: {totalInspected}</h3>
            <h3>Defective: {defectCount}</h3>
            <h3>Non-Defective: {nonDefectiveCount}</h3>

            <h3>Detection Logs</h3>
            <ul>
                {logs.map((log, index) => (
                    <li key={index}>{log}</li>
                ))}
            </ul>

            <h3>Inspection History</h3>
            <select onChange={(e) => setTimeFilter(e.target.value)} value={timeFilter}>
                <option value="today">Today</option>
                <option value="yesterday">Yesterday</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
            </select>
            <canvas id="historyChart"></canvas>
        </div>
    );
};

export default LiveWebcamMonitoring;