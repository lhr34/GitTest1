import os

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib


def train_power_model():

    df = pd.read_csv('data/dataset/sensor_data.csv')
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    features = df[['PowerSensor', 'TemperatureSensor', 'HumiditySensor', 'LightSensor', 'hour']]
    labels = df['power_consumption_level']

    # labeling data
    le = LabelEncoder()
    y = le.fit_transform(labels)

    # seperate training and testing dataset
    X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.2, random_state=42)

    '''Using Random Forest Classifier to train a model that 
    takes the sensor input data and classifies them to 3 power class'''

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        class_weight='balanced',
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(f'\nTest accuracy: {accuracy_score(y_test, y_pred):.2f}')

    # save the trained model locally
    MODEL_DIR = "ML_Model"
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(MODEL_DIR, "rf_power_model.pkl"))
    joblib.dump(le, os.path.join(MODEL_DIR, "label_encoder.pkl"))

    return model, le


if __name__ == "__main__":
    train_power_model()