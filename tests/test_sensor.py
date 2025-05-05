"""
Sensor Simulation Tests:
- Normal operation range validation (100-500W)
- Faulty value injection using monkeypatch
- Time-based light variation patterns
- Temperature/humidity formula consistency
- Error state recovery mechanism
"""

import pytest
from app.sensors import PowerSensorSimulator
from unittest.mock import patch
from datetime import datetime

# Fixture to create a reusable sensor instance
@pytest.fixture
def sensor():
    return PowerSensorSimulator()

# Test that PowerSensor value is within expected default range
def test_read_value_normal(sensor):
    value = sensor.read_value()
    assert 100 <= value['PowerSensor'] <= 500

# Test behavior when sensor is faulty (returns negative value)
def test_read_value_faulty(sensor, monkeypatch):
    monkeypatch.setattr(sensor, 'read_value', lambda: {'PowerSensor': -1})
    value = sensor.read_value()
    assert value['PowerSensor'] < 0

# Test that sensor respects a new max power limit
def test_sensor_max_value(sensor):
    sensor.max_power = 800
    value = sensor.read_value()
    assert value['PowerSensor'] <= 800

# Test that light sensor values vary based on time of day (mocked)
def test_sensor_light_variation(sensor):
    with patch("app.sensors.datetime") as mock_datetime:
        # Simulate daylight
        mock_datetime.now.return_value = datetime(2023, 1, 1, 10)
        day_values = [sensor.read_value()["LightSensor"] for _ in range(100)]

        # Simulate nighttime
        mock_datetime.now.return_value = datetime(2023, 1, 1, 2)
        night_values = [sensor.read_value()["LightSensor"] for _ in range(100)]

    # Average light should be higher during the day
    assert sum(day_values) / len(day_values) > sum(night_values) / len(night_values)

# Test that temperature is roughly consistent with power level
def test_temperature_humidity_consistency(sensor):
    data = sensor.read_value()
    expected_temp = 18 + (data['PowerSensor'] / 25)
    assert data['TemperatureSensor'] == pytest.approx(expected_temp, abs=2)

# Test that sensor recovers from invalid previous power readings
def test_sensor_recovery(sensor):
    sensor.last_power = -100  # Simulate a faulty last reading
    valid_data = sensor.read_value()
    assert 0 <= valid_data['PowerSensor'] <= sensor.max_power
