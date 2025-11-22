import React, { useEffect, useState } from "react";
import axios from "axios";

function HistoryPage() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/history/")
      .then((response) => {
        setHistory(response.data.history);
      })
      .catch((err) => {
        console.error("Error fetching history", err);
      });
  }, []);

  return (
    <div style={{ padding: "40px", maxWidth: "900px", margin: "auto" }}>
      <h2 style={{ marginBottom: "20px" }}>Recent Upload History</h2>

      {history.length === 0 ? (
        <p>No history available.</p>
      ) : (
        <table style={{
          width: "100%",
          borderCollapse: "collapse",
          background: "#fff",
          boxShadow: "0 0 8px rgba(0,0,0,0.1)",
          borderRadius: "8px",
          overflow: "hidden"
        }}>
          <thead style={{ background: "#f0f0f0" }}>
            <tr>
              <th style={thStyle}>Filename</th>
              <th style={thStyle}>Uploaded At</th>
              <th style={thStyle}>Total</th>
              <th style={thStyle}>Avg Flow</th>
              <th style={thStyle}>Avg Pressure</th>
              <th style={thStyle}>Avg Temp</th>
            </tr>
          </thead>

          <tbody>
            {history.map((item, index) => (
              <tr key={index}>
                <td style={tdStyle}>{item.filename}</td>
                <td style={tdStyle}>
                  {new Date(item.uploaded_at).toLocaleString()}
                </td>
                <td style={tdStyle}>{item.total_records}</td>
                <td style={tdStyle}>{item.avg_flowrate.toFixed(2)}</td>
                <td style={tdStyle}>{item.avg_pressure.toFixed(2)}</td>
                <td style={tdStyle}>{item.avg_temperature.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

const thStyle = {
  padding: "12px",
  fontWeight: "bold",
  textAlign: "left",
  borderBottom: "1px solid #ddd"
};

const tdStyle = {
  padding: "12px",
  borderBottom: "1px solid #eee"
};

export default HistoryPage;
