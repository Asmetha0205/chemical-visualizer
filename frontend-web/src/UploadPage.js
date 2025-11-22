import React, { useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale } from "chart.js";
import "./UploadPage.css";

ChartJS.register(BarElement, CategoryScale, LinearScale);

function UploadPage() {
  const [summary, setSummary] = useState(null);

  const handleUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/upload/",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      // backend sends: { message: "...", summary: {...} }
      setSummary(response.data.summary);

    } catch (error) {
      alert("Upload failed!");
      console.log(error);
    }
  };

  return (
    <div className="upload-page">
      <div className="upload-section">
        <h2 className="section-title">Upload CSV File</h2>
        <div className="file-upload-wrapper">
          <input 
            type="file" 
            accept=".csv"
            onChange={handleUpload}
            id="file-upload"
            className="file-upload-input"
          />
          <label htmlFor="file-upload" className="file-upload-label">
            <span className="file-upload-icon">📁</span>
            <span className="file-upload-text">Choose CSV File</span>
          </label>
        </div>
      </div>

      {summary && (
        <div className="summary-section">
          <div className="summary-card">
            <h3 className="card-title">Summary Statistics</h3>
            <div className="summary-grid">
              <div className="summary-item">
                <span className="summary-label">Total Equipment</span>
                <span className="summary-value">{summary.total_records}</span>
              </div>
              <div className="summary-item">
                <span className="summary-label">Average Flowrate</span>
                <span className="summary-value">{summary.avg_flowrate}</span>
              </div>
              <div className="summary-item">
                <span className="summary-label">Average Pressure</span>
                <span className="summary-value">{summary.avg_pressure}</span>
              </div>
              <div className="summary-item">
                <span className="summary-label">Average Temperature</span>
                <span className="summary-value">{summary.avg_temperature}</span>
              </div>
            </div>
          </div>

          <div className="chart-section">
            <h3 className="card-title">Equipment Type Distribution</h3>
            <div className="chart-container">
              <Bar
                data={{
                  labels: Object.keys(summary.type_distribution),
                  datasets: [
                    {
                      label: "Count",
                      data: Object.values(summary.type_distribution),
                      backgroundColor: "rgba(135, 206, 250, 0.6)",
                      borderColor: "rgba(135, 206, 250, 1)",
                      borderWidth: 2,
                      borderRadius: 8,
                    },
                  ]
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      display: false,
                    },
                  },
                  scales: {
                    y: {
                      beginAtZero: true,
                      grid: {
                        color: "rgba(135, 206, 250, 0.2)",
                      },
                    },
                    x: {
                      grid: {
                        color: "rgba(135, 206, 250, 0.2)",
                      },
                    },
                  },
                }}
                height={300}
              />
            </div>
          </div>
        </div>
      )}

      {summary && (
        <div className="button-section">
          <button
            onClick={() => window.open("http://127.0.0.1:8000/api/report/", "_blank")}
            className="download-button"
          >
            <span className="button-icon">📄</span>
            Download PDF Report
          </button>
        </div>
      )}
    </div>
  );
}

export default UploadPage;
