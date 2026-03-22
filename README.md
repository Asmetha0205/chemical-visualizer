**Chemical Equipment Parameter Visualizer**

Hybrid Web + Desktop Application
FOSSEE Winter Internship Screening Task (2025)

> 1. Overview

This project is a hybrid application consisting of a Django REST backend, a React.js web application, and a PyQt5 desktop application.
Users can upload a CSV file containing chemical equipment data. The backend processes it, generates summary statistics, stores history, and provides a PDF summary report.

> 2. Features

Backend
CSV upload API
Summary statistics (Flowrate, Pressure, Temperature)
Equipment type distribution
Store last 5 uploads (SQLite)
PDF report generation using ReportLab
Basic authentication API

Web Frontend (React)
CSV upload
Summary display
Bar chart (Chart.js)
History page
PDF download

Desktop Application (PyQt5)
CSV upload
Summary display
Matplotlib chart
History panel
PDF download

> 3. Tech Stack

Backend: Django, DRF, Pandas, ReportLab, SQLite
Web: React.js, Axios, Chart.js
Desktop: PyQt5, Matplotlib, Requests

> 4. Running the Project
   
Backend
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Web Frontend
cd frontend-web
npm install
npm start

Desktop
cd frontend-desktop
python desktop_app.py

> 5. API Endpoints
   
Method Endpoint Description
POST /api/upload/ Upload CSV & return summary
GET /api/history/ Get last 5 uploads
GET /api/report/ Download latest PDF report
POST /api/login/ Basic authentication

> 6. Authentication
   
A basic login API is included in the backend:
POST /api/login/
{ "username": "", "password": "" }

> 7. Author
    
Asmetha SureshBabu Thoppe
B.Tech CSE, 3rd Year
