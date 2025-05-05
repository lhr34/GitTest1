# app/data_store.py

import csv
import os
from datetime import datetime

# Define the default path for storing the power log data as a CSV file.
# This file contains all sensor readings appended over time.
LOG_FILE = "app/static/power_log.csv"


def append_log(data, building="Unknown"):
    """
    Appends a single sensor data entry to the power log CSV file.
    Parameters:
        data (dict): A dictionary containing sensor values with the following keys:
            - 'timestamp': The timestamp when the data was recorded.
            - 'PowerSensor': The power usage value in watts.
            - 'TemperatureSensor': Temperature value in Celsius.
            - 'HumiditySensor': Humidity percentage.
            - 'LightSensor': Light level in lux.
        building (str): Optional name of the building where the sensors are located. Default is "Unknown".
    If the log file does not exist, a header row is automatically written.
    """
    file_exists = os.path.isfile(LOG_FILE)

    # Open the CSV file in append mode; newline="" prevents blank lines on Windows.
    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp", "building", "PowerSensor", "TemperatureSensor", "HumiditySensor", "LightSensor"
        ])

        # If the file is newly created, write the header first
        if not file_exists:
            writer.writeheader()

        # Write a single row of sensor data to the CSV
        writer.writerow({
            "timestamp": data["timestamp"],
            "building": building,
            "PowerSensor": data["PowerSensor"],
            "TemperatureSensor": data["TemperatureSensor"],
            "HumiditySensor": data["HumiditySensor"],
            "LightSensor": data["LightSensor"]
        })


def read_logs():
    """
    Reads all entries from the power log CSV file and returns them as a list of dictionaries.

    Each dictionary represents one row from the CSV file, mapping column names to values.
    Whitespace is stripped from field names to handle inconsistencies caused by editing or export issues.

    Returns:
        List[dict]: A list of cleaned log entries. If the file does not exist, returns an empty list.
    """
    logs = []

    # Check if log file exists; return empty list if it doesn't
    if not os.path.exists(LOG_FILE):
        return logs

    with open(LOG_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Clean field names by stripping leading/trailing whitespace
            # This prevents issues with inconsistent headers (e.g., " PowerSensor" vs "PowerSensor")
            cleaned_row = {k.strip(): v for k, v in row.items()}
            logs.append(cleaned_row)

    return logs
