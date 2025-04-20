import csv
from datetime import datetime
import os

LOG_FILE = "data/power_log.csv"

HEADERS = ['timestamp', 'building', 'power', 'temperature', 'humidity', 'light']

def ensure_log_file():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)

def append_log(data: dict, building="Main Library"):
    ensure_log_file()
    with open(LOG_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            data['timestamp'], building,
            data['PowerSensor'], data['TemperatureSensor'],
            data['HumiditySensor'], data['LightSensor']
        ])

def read_logs():
    ensure_log_file()
    with open(LOG_FILE, newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)
