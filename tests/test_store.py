"""
Data Storage Tests:
- Temporary file logging isolation
- CSV append/read operations validation
- Global config preservation during tests
"""

import os
import tempfile
from app.data_store import append_log, read_logs
from unittest.mock import patch

def test_log_operations():
    # Create a temporary directory for test isolation
    with tempfile.TemporaryDirectory() as tmpdir:
        test_path = os.path.join(tmpdir, "test_log.csv")

        # Sample sensor data to append to the log
        test_data = {
            'timestamp': '2023-01-01T12:00:00',
            'PowerSensor': 250,
            'TemperatureSensor': 22,
            'HumiditySensor': 60,
            'LightSensor': 500
        }

        # Patch the LOG_FILE path used in app.data_store to use our temp file
        with patch("app.data_store.LOG_FILE", test_path):
            append_log(test_data)       # Write the test data
            logs = read_logs()          # Read the data back

            # Assertions to verify the data was logged correctly
            assert len(logs) == 1
            assert logs[0]["PowerSensor"] == "250"  # CSV data is read as strings
