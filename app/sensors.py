# app/sensors.py
import random

class PowerSensorSimulator:
    def __init__(self):
        self.current_value = 0

    def read_value(self):
        """
        Simulate sensor reading.
        Generate a random power consumption value between 100 and 500 Watts.
        """
        self.current_value = random.randint(100, 500)
        return self.current_value
