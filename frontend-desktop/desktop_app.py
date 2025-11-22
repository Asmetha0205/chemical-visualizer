import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QGroupBox, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
import matplotlib.pyplot as plt

BACKEND_URL = "http://127.0.0.1:8000/api"

class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chemical Visualizer (Desktop)")
        self.setGeometry(200, 200, 650, 650)
        
        # Apply modern styling
        self.apply_styles()

        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        self.label = QLabel("Chemical Equipment Visualizer")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.label.setFont(title_font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #2c3e50; padding: 10px;")
        main_layout.addWidget(self.label)

        subtitle = QLabel("Upload a CSV file to visualize your data")
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #7f8c8d; padding-bottom: 5px;")
        main_layout.addWidget(subtitle)

        # Upload button
        self.upload_button = QPushButton("Upload CSV File")
        button_font = QFont()
        button_font.setPointSize(11)
        button_font.setBold(True)
        self.upload_button.setFont(button_font)
        self.upload_button.setMinimumHeight(45)
        self.upload_button.setMinimumWidth(220)
        self.upload_button.clicked.connect(self.upload_csv)
        self.upload_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #87ceeb, stop:1 #5fb3d3);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5fb3d3, stop:1 #4a9bc4);
            }
        """)
        main_layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)

        # ❗ SUMMARY GROUP BOX
        self.summary_group = QGroupBox("Summary Statistics")
        summary_group_font = QFont()
        summary_group_font.setPointSize(13)
        summary_group_font.setBold(True)
        self.summary_group.setFont(summary_group_font)
        self.summary_group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #b0e0e6;
                border-radius: 10px;
                padding-top: 15px;
                background-color: #f8fbfc;
            }
            QGroupBox::title {
                padding: 0 5px;
                color: #2c3e50;
            }
        """)
        
        summary_layout = QVBoxLayout()
        summary_layout.setSpacing(12)
        summary_layout.setContentsMargins(20, 25, 20, 20)
        
        self.summary_label = QLabel("No data uploaded yet.")
        summary_label_font = QFont()
        summary_label_font.setPointSize(10)
        self.summary_label.setFont(summary_label_font)
        self.summary_label.setStyleSheet("color: #7f8c8d; padding: 5px;")
        summary_layout.addWidget(self.summary_label)
        
        self.summary_group.setLayout(summary_layout)
        main_layout.addWidget(self.summary_group)

        # ❗ HISTORY BUTTON
        self.history_button = QPushButton("Show Upload History")
        self.history_button.setFont(button_font)
        self.history_button.setMinimumHeight(42)
        self.history_button.clicked.connect(self.show_history)
        self.history_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c7ceea, stop:1 #a3b1ec);
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a3b1ec, stop:1 #8e9ddf);
            }
        """)
        main_layout.addWidget(self.history_button, alignment=Qt.AlignCenter)

        # ❗ HISTORY DISPLAY GROUP
        self.history_group = QGroupBox("Upload History (Last 5)")
        history_font = QFont()
        history_font.setPointSize(12)
        history_font.setBold(True)
        self.history_group.setFont(history_font)
        self.history_group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #ffd3a5;
                border-radius: 10px;
                padding-top: 15px;
                background-color: #fffaf5;
            }
            QGroupBox::title {
                padding: 0 5px;
                color: #d35400;
            }
        """)

        history_layout = QVBoxLayout()
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setStyleSheet("background: white; padding: 10px;")
        history_layout.addWidget(self.history_text)

        self.history_group.setLayout(history_layout)
        main_layout.addWidget(self.history_group)

        # ❗ CHART + PDF BUTTONS
        buttons_layout = QHBoxLayout()

        # Chart button
        self.chart_button = QPushButton("Show Chart")
        self.chart_button.setFont(button_font)
        self.chart_button.setMinimumHeight(42)
        self.chart_button.clicked.connect(self.show_chart)
        self.chart_button.setEnabled(False)
        buttons_layout.addWidget(self.chart_button)

        # PDF button
        self.pdf_button = QPushButton("Download PDF Report")
        self.pdf_button.setFont(button_font)
        self.pdf_button.setMinimumHeight(42)
        self.pdf_button.clicked.connect(self.download_pdf)
        self.pdf_button.setEnabled(False)
        buttons_layout.addWidget(self.pdf_button)

        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.summary = None

    def apply_styles(self):
        self.setStyleSheet("QWidget { background-color: #f5f9fa; }")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(245, 249, 250))
        palette.setColor(QPalette.WindowText, QColor(44, 62, 80))
        self.setPalette(palette)

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if not file_path:
            return

        response = requests.post(f"{BACKEND_URL}/upload/", files={"file": open(file_path, "rb")})

        if response.status_code == 200:
            data = response.json()
            self.summary = data["summary"]

            self.summary_label.setText(
                f"<b>Total:</b> {self.summary['total_records']}<br>"
                f"<b>Avg Flowrate:</b> {self.summary['avg_flowrate']}<br>"
                f"<b>Avg Pressure:</b> {self.summary['avg_pressure']}<br>"
                f"<b>Avg Temperature:</b> {self.summary['avg_temperature']}"
            )
            self.summary_label.setStyleSheet("color: #2c3e50; padding: 5px;")
            self.chart_button.setEnabled(True)
            self.pdf_button.setEnabled(True)

    def show_chart(self):
        if not self.summary:
            return
        
        types = list(self.summary["type_distribution"].keys())
        counts = list(self.summary["type_distribution"].values())

        plt.bar(types, counts, color=['#87ceeb', '#a8e6cf', '#ffd3a5', '#c7ceea'])
        plt.title("Equipment Type Distribution")
        plt.xlabel("Type")
        plt.ylabel("Count")
        plt.show()

    def download_pdf(self):
        import webbrowser
        webbrowser.open(f"{BACKEND_URL}/report/")

    def show_history(self):
        try:
            res = requests.get(f"{BACKEND_URL}/history/")
            history = res.json().get("history", [])

            if not history:
                self.history_text.setText("No history available.")
                return
            
            formatted = ""
            for h in history:
                formatted += (
                    f"<b>File:</b> {h['filename']}<br>"
                    f"<b>Uploaded At:</b> {h['uploaded_at']}<br>"
                    f"<b>Total Records:</b> {h['total_records']}<br>"
                    f"<b>Avg Flowrate:</b> {h['avg_flowrate']}<br>"
                    f"<b>Avg Pressure:</b> {h['avg_pressure']}<br>"
                    f"<b>Avg Temperature:</b> {h['avg_temperature']}<br>"
                    f"<b>Type Dist:</b> {h['type_distribution']}<br>"
                    "<hr>"
                )

            self.history_text.setHtml(formatted)

        except Exception as e:
            self.history_text.setText(f"Error fetching history: {e}")


app = QApplication(sys.argv)
window = DesktopApp()
window.show()
sys.exit(app.exec_())
