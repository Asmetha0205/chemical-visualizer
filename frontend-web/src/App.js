import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import UploadPage from "./UploadPage";
import HistoryPage from "./HistoryPage";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="app-container">
        <nav className="navbar">
          <div className="navbar-content">
            <h1 className="navbar-title">Chemical Equipment Visualizer</h1>

            <div className="navbar-links">
              <Link className="nav-link" to="/">Upload</Link>
              <Link className="nav-link" to="/history">History</Link>
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<UploadPage />} />
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
