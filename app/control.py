from abc import ABC, abstractmethod
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


class ControlStrategy(ABC):
    @abstractmethod
    def control_action(self, data):
        pass

# using Adaptor design pattern to incompatible manuel control and auto control strategy
class AutoControlStrategy(ControlStrategy):
    # using the trained RandomForest control model
    def __init__(self):
        try:
            self.model = joblib.load('app/ML_model/rf_power_model.pkl')
            self.le = joblib.load('app/ML_model/label_encoder.pkl')
        except FileNotFoundError:
            print("Warning: Model files not found. Using fallback prediction logic.")
            self.model = None
            self.le = None

        self.control_rules = {
            'low': "Power usage: Low;\n Action: Reduce power supply to energy saving mode",
            'normal': "Power usage: Normal;\n Action: Maintain current power supply level",
            'high': "Power usage: High;\n Action: Start the backup power supply",
            'abnormal': "Power usage: Abnormal;\n Action: Emergency cut-off of non-critical loads and alarm"
        }

    def _prepare_features(self, data_dict):
        timestamp = pd.to_datetime(data_dict['timestamp'])
        return pd.DataFrame([{
            'PowerSensor': data_dict['PowerSensor'],
            'TemperatureSensor': data_dict['TemperatureSensor'],
            'HumiditySensor': data_dict['HumiditySensor'],
            'LightSensor': data_dict['LightSensor'],
            'hour': timestamp.hour
        }])

    def control_action(self, data):
        try:
            if self.model is None:
                # Fallback logic if model isn't loaded
                power = data['PowerSensor']
                if power < 150:
                    level = 'low'
                elif power < 500:
                    level = 'normal'
                elif power < 700:
                    level = 'high'
                else:
                    level = 'abnormal'
            else:
                features = self._prepare_features(data)
                pred = self.model.predict(features)[0]
                level = self.le.inverse_transform([pred])[0]
            return self.control_rules.get(level, "unknown action")

        except Exception as e:
            print(f"control error: {str(e)}")
            return "control error，please switch to manuel control"


class ManualControlStrategy(ControlStrategy):
    def __init__(self, mode="normal"):
        self.set_mode(mode)

    def set_mode(self, mode):
        self.mode = mode
        self.control_actions = {
            "eco": "Manual Control: ECO MODE\nAction: Limiting power consumption to 30%, non-essential systems disabled",
            "normal": "Manual Control: NORMAL MODE\nAction: Standard power distribution across all systems",
            "full-power": "Manual Control: FULL-POWER MODE\nAction: Maximum power allocation to all systems, cooling increased"
        }

    def control_action(self, data):
        return self.control_actions.get(self.mode, "Unknown mode, fallback to normal operation")


class PowerControlContext:
    def __init__(self, strategy: ControlStrategy = None):
        self.strategy = strategy or AutoControlStrategy()

    def set_strategy(self, strategy: ControlStrategy):
        self.strategy = strategy

    def execute_control(self, data):
        return self.strategy.control_action(data)


