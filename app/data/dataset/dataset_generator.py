import csv
from datetime import timedelta, datetime
import random

import csv
from datetime import timedelta, datetime
import random


def determine_level(row):
    """
    row: 包含各传感器值的字典
    返回: low/normal/high/abnormal
    """
    power = row['PowerSensor']
    temp = row['TemperatureSensor']
    humidity = row['HumiditySensor']
    light = row['LightSensor']
    hour = datetime.fromisoformat(row['timestamp']).hour

    # 新阈值体系（0-800W范围）
    if power < 150:
        base_level = 'low'
    elif 150 <= power <= 500:
        base_level = 'normal'
    elif 500 < power <= 700:
        base_level = 'high'
    else:
        return 'abnormal'  # 超过700W视为异常

    # 环境矛盾检测规则
    anomalies = []

    # 高温低功率检测（空调异常）
    if temp > 35 and power < 400:  # 温度阈值提高
        anomalies.append('temp_power_mismatch')

    # 高湿度检测（除湿系统失效）
    if humidity > 80 and power < 300:  # 湿度阈值调整
        anomalies.append('humidity_power_mismatch')

    # 异常照明检测
    if not (6 <= hour <= 20) and light > 500:  # 扩大白天时间范围
        anomalies.append('night_light_abnormal')

    # 设备过载模式检测
    overload_conditions = [
        power > 650 and temp > 40,  # 更高功率+极端高温
        power > 600 and humidity < 20,  # 高功率+极度干燥
        power > 550 and light < 300  # 中等高功率+异常低光照
    ]

    # 综合判定逻辑
    if len(anomalies) >= 1 or any(overload_conditions):
        return 'abnormal'
    elif power > 700:  # 绝对上限保护
        return 'abnormal'
    else:
        return base_level

def _generate_light(hour):
    """生成符合昼夜规律的光照数据"""
    if 6 <= hour <= 20:  # 白天时间6:00-20:00
        base = random.randint(800, 2500)
        return base - abs(13 - hour) * 100  # 正午13点达到峰值
    else:  # 夜间
        return random.randint(0, 500)


def generate_data(size):
    base_time = datetime(2023, 10, 1, 8, 0)
    dataset = []

    for _ in range(size):
        time_step = timedelta(minutes=15)
        hour = base_time.hour

        # 生成基础参数（0-800W范围）
        power = random.uniform(0, 800)  # 基础功率范围扩大

        # 温度公式调整（15-45°C范围）
        temp = 15 + (power / 30) + random.uniform(-2, 2)

        # 湿度公式调整（20-90%范围）
        humidity = 70 - (power / 30) + random.uniform(-10, 10)

        # 光照生成逻辑增强
        light = _generate_light(hour) if hour else 0

        # 注入新型异常模式
        if _ % 50 == 0:  # 每50条插入一个异常
            if random.choice([True, False]):
                # 类型1：极端高功率
                power = random.uniform(750, 850)
            else:
                # 类型2：环境参数矛盾
                temp = 45 + random.uniform(0, 5)
                humidity = 10 + random.uniform(0, 5)

        # 数值裁剪（确保物理合理性）
        power = round(max(0, min(800, power)), 1)
        temp = round(max(10, min(50, temp)), 1)
        humidity = round(max(5, min(95, humidity)), 1)
        light = round(max(0, min(2500, light)), 1)

        row = {
            'timestamp': base_time.isoformat(),
            'PowerSensor': power,
            'TemperatureSensor': temp,
            'HumiditySensor': humidity,
            'LightSensor': light,
            'power_consumption': power
        }
        row['power_consumption_level'] = determine_level(row)

        dataset.append(row)
        base_time += time_step

    return dataset



headers = ['timestamp', 'PowerSensor', 'TemperatureSensor',
           'HumiditySensor', 'LightSensor', 'power_consumption',
           'power_consumption_level']

data = generate_data(500)
with open('sensor_data.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)

print("Dataset 'sensor_data.csv' Is Successfully Generated!")
