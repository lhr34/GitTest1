from app.control import AutoControlStrategy, ManualControlStrategy
import pytest
from unittest.mock import patch


def test_auto_control_fallback():
    strategy = AutoControlStrategy()
    strategy.model = None

    test_data = {'PowerSensor': 100, 'timestamp': '2023-01-01T12:00:00',
                 'TemperatureSensor': 25, 'HumiditySensor': 50, 'LightSensor': 300}
    result = strategy.control_action(test_data)
    assert "Reduce power supply" in result


def test_manual_control_modes():
    manual = ManualControlStrategy(mode="eco")
    assert "ECO MODE" in manual.control_action({})


@patch('joblib.load')
def test_auto_control_with_model(mock_load):

    mock_model = mock_load.return_value
    mock_model.predict.return_value = [0]
    mock_label_encoder = mock_load.return_value
    mock_label_encoder.inverse_transform.return_value = ['low']

    strategy = AutoControlStrategy()
    test_data = {'PowerSensor': 100, 'timestamp': '2023-01-01T12:00:00',
                 'TemperatureSensor': 25, 'HumiditySensor': 50, 'LightSensor': 300}
    result = strategy.control_action(test_data)
    assert "Reduce power supply" in result