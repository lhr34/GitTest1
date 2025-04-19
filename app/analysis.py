# app/analysis.py
class AnalysisEngine:
    def __init__(self, threshold):
        """
        threshold: A threshold value (in Watts) above which data is considered anomalous.
        """
        self.threshold = threshold

    # app/analysis.py
    def analyze(self, power_history):  # 统一参数名
        alerts = []
        for data in power_history:
            if data > self.threshold:
                alerts.append(data)
        return alerts

    def generate_trend_report(self, power_history):  # 统一参数名
        if not power_history:
            return "No data to generate report."
        average = sum(power_history) / len(power_history)
        return f"Trend Report: Average power consumption = {average:.2f} Watts"
