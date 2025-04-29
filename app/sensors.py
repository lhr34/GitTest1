import random
from datetime import datetime

# the prototype is running on simulated sensor data
class PowerSensorSimulator:
    def __init__(self):
        self.last_power = 400
        self.max_power = 800
        self.min_power = 0

    # generate sensor reading in a normal pattern
    def _generate_light(self, hour):
        if 8 <= hour <= 18:
            base = random.randint(800, 2000)
            return base - abs(13 - hour) * 100
        else:
            return random.randint(0, 300) + random.randint(0, 50)

    def _generate_power(self):
        fluctuation = random.randint(-200, 200)
        new_power = self.last_power + fluctuation
        new_power = max(self.min_power, min(self.max_power, new_power))
        if new_power < 50:
            new_power += random.randint(50, 150)
        elif new_power > 750:
            new_power -= random.randint(50, 150)
        return new_power

    def read_value(self):
        self.last_power = self._generate_power()
        timestamp = datetime.now().isoformat()
        hour = datetime.now().hour
        return {
            "timestamp": timestamp,
            "PowerSensor": self.last_power,
            "TemperatureSensor": round(18 + (self.last_power / 25) + random.uniform(-1, 1)),
            "HumiditySensor": round(65 - (self.last_power / 20) + random.randint(-5, 5)),
            "LightSensor": self._generate_light(hour),
            "power_consumption": self.last_power
        }

