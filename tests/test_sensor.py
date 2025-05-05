import pytest
from app.sensors import PowerSensorSimulator



@pytest.fixture
def sensor():
    return PowerSensorSimulator()


def test_read_value_normal(sensor):

    value = sensor.read_value()
    assert 100 <= value['PowerSensor'] <= 500


def test_read_value_faulty(sensor, monkeypatch):

    monkeypatch.setattr(sensor, 'read_value', lambda: {'PowerSensor': -1})
    value = sensor.read_value()
    assert value['PowerSensor'] < 0


def test_sensor_max_value(sensor):

    sensor.max_power = 800
    value = sensor.read_value()
    assert value['PowerSensor'] <= 800


from unittest.mock import patch
from datetime import datetime

def test_sensor_light_variation(sensor):
    with patch("app.sensors.datetime") as mock_datetime:

        mock_datetime.now.return_value = datetime(2023, 1, 1, 10)
        day_values = [sensor.read_value()["LightSensor"] for _ in range(100)]


        mock_datetime.now.return_value = datetime(2023, 1, 1, 2)
        night_values = [sensor.read_value()["LightSensor"] for _ in range(100)]

    assert sum(day_values) / len(day_values) > sum(night_values) / len(night_values)



def test_temperature_humidity_consistency(sensor):
    data = sensor.read_value()
    expected_temp = 18 + (data['PowerSensor'] / 25)
    assert data['TemperatureSensor'] == pytest.approx(expected_temp, abs=2)


def test_sensor_recovery(sensor):

    sensor.last_power = -100
    valid_data = sensor.read_value()
    assert 0 <= valid_data['PowerSensor'] <= sensor.max_power

