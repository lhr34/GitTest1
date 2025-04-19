# app/training.py
import os

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib


def train_power_model():
    # 加载数据集
    df = pd.read_csv('data/dataset/sensor_data.csv')

    # 特征工程
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    features = df[['PowerSensor', 'TemperatureSensor', 'HumiditySensor', 'LightSensor', 'hour']]
    labels = df['power_consumption_level']

    # 编码标签
    le = LabelEncoder()
    y = le.fit_transform(labels)

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.2, random_state=42)

    # 构建随机森林模型
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        class_weight='balanced',
        random_state=42
    )

    # 训练模型
    model.fit(X_train, y_train)

    # 评估模型
    y_pred = model.predict(X_test)
    print(f'\nTest accuracy: {accuracy_score(y_test, y_pred):.2f}')

    # 保存模型和编码器

    MODEL_DIR = "ML_Model"  # 可修改為你的目標路徑
    os.makedirs(MODEL_DIR, exist_ok=True)

    # 保存模型和編碼器到指定路徑
    joblib.dump(model, os.path.join(MODEL_DIR, "rf_power_model.pkl"))
    joblib.dump(le, os.path.join(MODEL_DIR, "label_encoder.pkl"))

    return model, le


if __name__ == "__main__":
    train_power_model()