"""
Control Strategy Tests:
- Auto control fallback without ML model
- Manual mode handling (ECO mode verification)
- Mocked ML model predictions integration test
"""

from app.control import AutoControlStrategy, ManualControlStrategy
import pytest
from unittest.mock import patch

# Test fallback behavior when the AutoControlStrategy has no ML model loaded
def test_auto_control_fallback():
    strategy = AutoControlStrategy()
    strategy.model = None  # Simulate the absence of a trained model

    test_data = {
        'PowerSensor': 100,
        'timestamp': '2023-01-01T12:00:00',
        'TemperatureSensor': 25,
        'HumiditySensor': 50,
        'LightSensor': 300
    }

    result = strategy.control_action(test_data)
    assert "Reduce power supply" in result  # Expect a default fallback message

# Test behavior of ManualControlStrategy under a specific mode
def test_manual_control_modes():
    manual = ManualControlStrategy(mode="eco")
    assert "ECO MODE" in manual.control_action({})  # Should reflect eco mode logic

# Mock model and label encoder used in AutoControlStrategy
@patch('joblib.load')
def test_auto_control_with_model(mock_load):
    # Mock the model's prediction
    mock_model = mock_load.return_value
    mock_model.predict.return_value = [0]

    # Mock the label encoder's output
    mock_label_encoder = mock_load.return_value
    mock_label_encoder.inverse_transform.return_value = ['low']

    strategy = AutoControlStrategy()
    strategy.model = mock_model
    strategy.label_encoder = mock_label_encoder

    test_data = {
        'PowerSensor': 100,
        'timestamp': '2023-01-01T12:00:00',
        'TemperatureSensor': 25,
        'HumiditySensor': 50,
        'LightSensor': 300
    }

    result = strategy.control_action(test_data)
    assert "low" in result  # Expect result to contain the decoded prediction label
