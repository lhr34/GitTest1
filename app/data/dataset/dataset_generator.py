import csv
from datetime import timedelta, datetime
import random

# this dataset generator simulates the data pattern in real life,and is used for training the Random Forest model
# the output is a csv file which can be easily convert into a dataframe and use for model training

def determine_level(row):
    power = row['PowerSensor']
    temp = row['TemperatureSensor']
    humidity = row['HumiditySensor']
    light = row['LightSensor']
    hour = datetime.fromisoformat(row['timestamp']).hour

    if power < 150:
        base_level = 'low'
    elif 150 <= power <= 500:
        base_level = 'normal'
    elif 500 < power <= 700:
        base_level = 'high'
    else:
        return 'abnormal'

    anomalies = []

    if temp > 35 and power < 400:
        anomalies.append('temp_power_mismatch')

    if humidity > 80 and power < 300:
        anomalies.append('humidity_power_mismatch')

    if not (6 <= hour <= 20) and light > 500:
        anomalies.append('night_light_abnormal')

    # 设备过载模式检测
    overload_conditions = [
        power > 650 and temp > 40,
        power > 600 and humidity < 20,
        power > 550 and light < 300
    ]

    # 综合判定逻辑
    if len(anomalies) >= 1 or any(overload_conditions):
        return 'abnormal'
    elif power > 700:
        return 'abnormal'
    else:
        return base_level

def _generate_light(hour):
    if 6 <= hour <= 20:
        base = random.randint(800, 2500)
        return base - abs(13 - hour) * 100
    else:
        return random.randint(0, 500)


def generate_data(size):
    base_time = datetime(2023, 10, 1, 8, 0)
    dataset = []

    for _ in range(size):
        time_step = timedelta(minutes=15)
        hour = base_time.hour

        power = random.uniform(0, 800)

        temp = 15 + (power / 30) + random.uniform(-2, 2)

        humidity = 70 - (power / 30) + random.uniform(-10, 10)

        light = _generate_light(hour) if hour else 0

        if _ % 50 == 0:
            if random.choice([True, False]):
                power = random.uniform(750, 850)
            else:
                temp = 45 + random.uniform(0, 5)
                humidity = 10 + random.uniform(0, 5)

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
