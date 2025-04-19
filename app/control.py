# app/control.py
from abc import ABC, abstractmethod
import joblib
import pandas as pd


class ControlStrategy(ABC):
    @abstractmethod
    def control_action(self, data):
        pass


class AutoControlStrategy(ControlStrategy):
    def __init__(self):
        # 加载训练好的模型和编码器
        self.model = joblib.load('app/ML_model/rf_power_model.pkl')
        self.le = joblib.load('app/ML_model/label_encoder.pkl')

        # 定义控制规则
        self.control_rules = {
            'low': "Power usage: Low;\n Action: Reduce power supply to energy saving mode",
            'normal': "Power usage: Normal;\n Action: Maintain current power supply level",
            'high': "Power usage: High;\n Action: Start the backup power supply",
            'abnormal': "Power usage: Abnormal;\n Action: Emergency cut-off of non-critical loads and alarm"
        }

    def _prepare_features(self, data_dict):
        """准备特征数据框"""
        timestamp = pd.to_datetime(data_dict['timestamp'])
        return pd.DataFrame([{
            'PowerSensor': data_dict['PowerSensor'],
            'TemperatureSensor': data_dict['TemperatureSensor'],
            'HumiditySensor': data_dict['HumiditySensor'],
            'LightSensor': data_dict['LightSensor'],
            'hour': timestamp.hour
        }])

    def control_action(self, data):
        try:
            # 准备特征数据
            features = self._prepare_features(data)

            # 模型预测
            pred = self.model.predict(features)[0]
            level = self.le.inverse_transform([pred])[0]

            # 获取控制指令
            return self.control_rules.get(level, "未知状态，启用安全模式")

        except Exception as e:
            print(f"预测错误: {str(e)}")
            return "系统异常，切换至手动模式"


class PowerControlContext:
    def __init__(self, strategy: ControlStrategy = None):
        self.strategy = strategy or AutoControlStrategy()

    def set_strategy(self, strategy: ControlStrategy):
        self.strategy = strategy

    def execute_control(self, data):
        return self.strategy.control_action(data)


# 保留原有备用策略
class FallbackControlStrategy(ControlStrategy):
    def control_action(self, data):
        if data['PowerSensor'] > 450:
            return "备用策略：切断非关键负载"
        return "备用策略：维持当前状态"