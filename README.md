# Smart Campus Power Management System

## Project Overview
The Smart Campus Power Management System is a web-based application designed to monitor, analyze, and control power usage across campus buildings. It simulates real-time power sensor readings along with environmental data (temperature, humidity, light), performs analysis to detect anomalies, and implements intelligent control strategies based on power consumption patterns. The system uses machine learning (Random Forest) to classify power usage into different levels and recommend appropriate control actions. This platform aims to optimize energy usage, reduce costs, and prevent overloads by providing automated management and manual override capabilities. With its simulation features, the system allows for testing different scenarios without affecting real-world operations, making it an ideal tool for both educational purposes and practical energy management planning.

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

4. **(First Time Running)Generate Dataset For Model Training **
   run 'app/data/dataset/dataset_generator.py'

5. **Run the application**
   ```bash
   flask run
   # or
   python run.py
   ```

6. **Access the web interface**
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

### Core Features
1. **Power Monitoring Simulation**
   - Real-time sensor data simulation
   - Environmental parameters tracking (temperature, humidity, light)
   
2. **Power Analysis**
   - Threshold-based anomaly detection
   - Trend analysis and reporting
   
3. **Intelligent Control**
   - ML-based automatic control recommendations
   - Manual control modes (Eco, Normal, Full-Power)
   
4. **Data Visualization**
   - Interactive power consumption charts
   - Real-time updates and countdowns
   
5. **Logging System**
   - Persistent data storage
   - Filterable log views
   - CSV export capabilities

### Additional Features
- Modular architecture with clear separation of concerns
- Object-oriented design with design patterns implementation
- Automated model training on startup

## Contribution

### Work Description
