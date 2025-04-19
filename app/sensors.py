# app/sensors.py
import random
from datetime import datetime


class PowerSensorSimulator:
    def __init__(self):
        self.last_power = 400  # 初始值设为中间值
        self.max_power = 800  # 最大功率限制
        self.min_power = 0  # 最小功率限制

    def _generate_light(self, hour):
        """生成符合昼夜规律的光照数据"""
        if 8 <= hour <= 18:  # 白天
            base = random.randint(800, 2000)
            return base - abs(13 - hour) * 100  # 正午最高
        else:  # 夜间
            return random.randint(0, 300) + random.randint(0, 50)  # 基础光照+随机波动

    def _generate_power(self):
        """生成合理范围内的功率值（0-800W）"""
        # 随机波动幅度（限制在±200W以内以保证连续性）
        fluctuation = random.randint(-200, 200)
        new_power = self.last_power + fluctuation

        # 确保功率在合理范围内
        new_power = max(self.min_power, min(self.max_power, new_power))

        # 避免长时间处于极端值
        if new_power < 50:
            new_power += random.randint(50, 150)
        elif new_power > 750:
            new_power -= random.randint(50, 150)

        return new_power

    def read_value(self):
        """生成包含多个传感器数据的字典"""
        # 更新功率值
        self.last_power = self._generate_power()

        # 生成基础时间戳
        timestamp = datetime.now().isoformat()

        # 根据电力数据生成相关传感器数据
        hour = datetime.now().hour
        return {
            "timestamp": timestamp,
            "PowerSensor": self.last_power,
            "TemperatureSensor": round(18 + (self.last_power / 25) + random.uniform(-1, 1)),
            "HumiditySensor": round(65 - (self.last_power / 20) + random.randint(-5, 5)),
            "LightSensor": self._generate_light(hour),
            "power_consumption": self.last_power
        }

