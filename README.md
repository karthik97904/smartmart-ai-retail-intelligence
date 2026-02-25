# SmartMart AI Retail Intelligence Platform

SmartMart is an AI-driven retail analytics and forecasting system designed to assist business decision-makers in monitoring performance, predicting sales trends, and generating executive-level strategic insights.

---

## 1. Project Overview

SmartMart provides:

- Sales forecasting using machine learning
- Profit driver and margin analysis
- Risk evaluation and trend monitoring
- Executive AI advisory interface
- Role-based authentication (CEO / HR)

The system is designed with a layered architecture and supports local AI execution using open-source models.

---

## 2. System Architecture

Application Flow:

Route → Service Layer → Repository Layer → AI Engine → Database

Technology Stack:

- Backend: Python (Flask)
- Database: MySQL
- ORM: SQLAlchemy
- Machine Learning: Scikit-learn (Linear Regression)
- Frontend: Bootstrap, Chart.js
- AI Model: Ollama (Phi)
- Authentication: Flask-Login

---

## 3. Core Modules

### 3.1 Sales Forecast Engine

- Linear Regression based forecasting
- Seasonal adjustment support
- Historical vs forecast comparison
- Confidence band visualization
- Accuracy measurement (MAPE)

### 3.2 CEO AI Advisor

- Interactive chat interface
- AI-based strategic reasoning
- Local LLM integration via Ollama
- Business-focused recommendations

### 3.3 Profit Driver Analysis

- Revenue contribution analysis
- Margin classification
- Loss-maker identification

### 3.4 Risk Intelligence

- Market stress assessment
- Risk and opportunity scoring

### 3.5 Role-Based Access Control

- CEO dashboard
- HR data management interface

---

## 4. Project Structure


smartmart/
│
├── app/
│ ├── api/
│ ├── services/
│ ├── repositories/
│ ├── ai_engine/
│ ├── models/
│
├── templates/
├── static/
├── migrations/
├── run.py
├── requirements.txt
└── README.md


---

## 5. Installation (Local Setup)

### 5.1 Clone Repository


git clone https://github.com/karthik97904/smartmart-ai-retail-intelligence.git

cd smartmart-ai-retail-intelligence


### 5.2 Create Virtual Environment


python -m venv venv
venv\Scripts\activate


### 5.3 Install Dependencies


pip install -r requirements.txt


### 5.4 Run Application


python run.py


Access the application at:


http://127.0.0.1:5000


---

## 6. Configuration

Ensure the following are properly configured:

- MySQL database connection
- Environment variables in `.env`
- Ollama installed and Phi model pulled


ollama pull phi


---

## 7. Future Improvements

- Advanced forecasting models (ARIMA, LSTM)
- Cloud deployment support
- Real-time data ingestion
- Executive KPI dashboard enhancements
- Streaming AI response support

---

## 8. Author

Karthikeyan M  
GitHub: https://github.com/karthik97904

---

## 9. License

This project is intended for academic and portfolio purposes.
