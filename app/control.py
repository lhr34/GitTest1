# app/control.py
from abc import ABC, abstractmethod

class ControlStrategy(ABC):
    @abstractmethod
    def control_action(self, data):
        pass

class AutoControlStrategy(ControlStrategy):
    def __init__(self, control_threshold):
        """
        control_threshold: When power consumption exceeds this value,
                           an action is taken to reduce the load.
        """
        self.control_threshold = control_threshold

    def control_action(self, data):
        if data > self.control_threshold:
            return "Auto Control: High power detected. Reducing load by turning off non-essential devices."
        else:
            return "Auto Control: Power consumption is normal. No action needed."

class ManualControlStrategy(ControlStrategy):
    def __init__(self, manual_setting):
        """
        manual_setting: A preset mode or parameter for manual control.
        """
        self.manual_setting = manual_setting

    def control_action(self, data):
        return f"Manual Control: Applying preset mode '{self.manual_setting}', ignoring current data."

class PowerControlContext:
    def __init__(self, strategy: ControlStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: ControlStrategy):
        self.strategy = strategy

    def execute_control(self, data):
        return self.strategy.control_action(data)
