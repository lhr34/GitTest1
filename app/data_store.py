# app/data_store.py

import csv
import os
from datetime import datetime

# 默认日志路径
LOG_FILE = "app/static/power_log.csv"

# 写入日志
def append_log(data, building="Unknown"):
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp", "building", "PowerSensor", "TemperatureSensor", "HumiditySensor", "LightSensor"
        ])

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": data["timestamp"],
            "building": building,
            "PowerSensor": data["PowerSensor"],
            "TemperatureSensor": data["TemperatureSensor"],
            "HumiditySensor": data["HumiditySensor"],
            "LightSensor": data["LightSensor"]
        })

# 读取日志（修复字段名问题）
def read_logs():
    logs = []
    if not os.path.exists(LOG_FILE):
        return logs

    with open(LOG_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 清理字段名：strip 去除空格，保留原始大小写
            cleaned_row = {k.strip(): v for k, v in row.items()}
            logs.append(cleaned_row)

    return logs
