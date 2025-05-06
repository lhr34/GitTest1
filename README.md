# Smart Campus Power Management System

## Project Overview
The Smart Campus Power Management System is a web-based application designed to track, analyze, and manage electricity consumption in real-time. It simulates sensor data and provides tools for anomaly detection, trend analysis, and automated control responses. The system features multiple control strategies, detailed analytics with severity classification, pattern detection, and consumption forecasting. It's suitable for building management systems, industrial power monitoring, or any scenario requiring intelligent power consumption oversight.

## Installation and Setup

### Prerequisites
- Python 3.10+ 
- pip (Python package manager)
- Git (optional)

### Step-by-Step Instructions

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   # or download and extract the ZIP file
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```
   
   If requirements.txt is not available, install the following packages:
   ```bash
   pip install flask flask-sqlalchemy flask-login scikit-learn pandas joblib
   ```

4. **(First Time Running)Generate Dataset For Model Training**
   ```bash
   python 'app/data/dataset/dataset_generator.py'
   ```

6. **Run the application**
   ```bash
   flask run
   # or
   python run.py
   ```

7. **Access the web interface**
   Open your browser and navigate to `http://127.0.0.1:5000`

## Technologies Used

### Programming Languages
- Python (Backend)
- JavaScript (Frontend charts/interactivity)
- HTML/CSS (Frontend structure/styling)

### Frameworks & Libraries
- Flask (Web framework)
- SQLAlchemy (ORM for database operations)
- Flask-Login (Authentication)
- Scikit-learn (Machine learning components)
- Pandas (Data manipulation)
- Joblib (Model serialization)
- Chart.js (Data visualization)
- Bootstrap 5 (Frontend styling)

## Implemented Functionalities

# Key Features

## Advanced Power Analytics

- **Threshold-based Alerts**: Detect anomalies when consumption exceeds configurable thresholds.
- **Severity Classification**: Categorize alerts into critical, high, moderate, and low based on excess percentage.
- **Trend Analysis**: Generate average, min/max, median, and standard deviation reports.
- **Pattern Detection**: Identify cyclic trends, spikes, and consistent increases/decreases using moving averages.
- **Consumption Forecasting**: Predict future usage with a weighted moving average model.

## Adaptive Control Strategies
- **Using real-time sensor data input to control power supply**
### Auto Mode
- Uses a trained Random Forest model for intelligent decision-making.
- Fallback to rule-based logic if models are unavailable (e.g., "Start backup power" for high usage).

### Manual Modes
- Allow the user to select 3 different power modes manually.

### Legacy Integration
- Adapter for compatibility with older `SimpleControlSystem`.

## Real-Time Monitoring & Observers

- **Live Dashboard**: Display sensor data (power, temperature, humidity, light).
- **Data Logging**: Capture and store historical readings with timestamps.
- **Observer Pattern**: Notify subscribers (e.g., dashboard, logger) on new data.

## Reporting & Diagnostics

- **Detailed Reports**: Include peak times, trend direction, and alert percentages.
- **CSV Export**: Download logs for offline analysis.
- **API Endpoints**: Fetch analytics (alerts, forecasts, patterns) in JSON format.

## Simulation & Testing

- **Sensor Simulator**: Generates realistic power, temperature, humidity, and light data.
- **Unit Tests**: Validate analysis logic, control strategies, user models, and data storage.
- **Test Report**: HTML report for pytest results (`report.html`).

## User Management

- Secure authentication with password hashing.
- Session-based control mode persistence.


## Contribution
| Student Name & ID | Contribution (%) | Key Contributions / Tasks Completed | Comments (if any) | Signature |
|--------|--------|--------|--------|--------|
|Hengrui Lu 2865255|25%|Backend: implement power control features; data generating and ML model training; <br>Frontend: power control panel; sensor data display; power consumption graph; <br>Other: README file|        |Hengrui Lu|
|        |        |        |        |        |
|        |        |        |        |        |
|        |        |        |        |        |
