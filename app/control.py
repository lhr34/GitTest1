from abc import ABC, abstractmethod
import joblib
import pandas as pd

# control.py defines all the control strategies that are used to control the power supply system
# since the interface of the power supply system is unknown,
# the control action is made by texts that can be further implementing into real control actions
# according to the power supply system

# ControlStrategy class is a base class that defines the interface for all control strategies
# each control strategies will rewrite the function control_action()
class ControlStrategy(ABC):
    @abstractmethod
    def control_action(self, data):
        pass

class AutoControlStrategy(ControlStrategy):
    # using the trained RandomForest control model
    def __init__(self):
        # Initialize the auto control strategy by loading the trained model and label encoder.
        # Fallback to simple rule-based logic if model files are missing.
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
        # Process raw sensor data into a DataFrame to compatible with the ML model.
        timestamp = pd.to_datetime(data_dict['timestamp'])
        return pd.DataFrame([{
            'PowerSensor': data_dict['PowerSensor'],
            'TemperatureSensor': data_dict['TemperatureSensor'],
            'HumiditySensor': data_dict['HumiditySensor'],
            'LightSensor': data_dict['LightSensor'],
            'hour': timestamp.hour
        }])

    def control_action(self, data):
        # rewrite parent class' control_action() function
        # execute control action using ML model
        # if no model loaded, use fallback rules
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
                # using ML model to control system
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
        # the manuel mode has 3 power modes to be manually select
        self.mode = mode
        self.control_actions = {
            "eco": "Manual Control: ECO MODE\nAction: Limiting power consumption to 30%, non-essential systems disabled",
            "normal": "Manual Control: NORMAL MODE\nAction: Standard power distribution across all systems",
            "full-power": "Manual Control: FULL-POWER MODE\nAction: Maximum power allocation to all systems, cooling increased"
        }

    def control_action(self, data):
        # by using flask form and view handler, user can update the control mode manually
        return self.control_actions.get(self.mode, "Unknown mode, fallback to normal operation")


# assume there is another outdated control strategy:SimpleControlSystem,
# which doesn't inherit ControlStrategy class, so it can't running control strategy directly like other strategies
class SimpleControlSystem:
    def simple_control(self, power_value):
        # works with simple power value only
        if power_value < 200:
            return "Simple Control System: Low power state activated"
        elif power_value < 600:
            return "Simple Control System: Normal operation"
        else:
            return "Simple Control System: High power alert, initiating simple protocols"


# to make this control strategy class works, we need to create an adapter
# that makes SimpleControlSystem compatible with ControlStrategy class
# which inherits ControlStrategy class and rewrites method control_action()
class SimpleControlAdapter(ControlStrategy):
    def __init__(self, simple_system):
        self.simple_system = simple_system

    def control_action(self, data):
        # Extract just the power value from the complex sensor data
        # and pass it to the simple system
        power_value = data['PowerSensor']
        return self.simple_system.simple_control(power_value)


class PowerControlContext:
    # PowerControlContext class to manage and execute the selected control strategy
    def __init__(self, strategy: ControlStrategy = None):
        self.strategy = strategy or AutoControlStrategy()

    def set_strategy(self, strategy: ControlStrategy):
        self.strategy = strategy

    def execute_control(self, data):
        return self.strategy.control_action(data)


