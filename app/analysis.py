# app/analysis.py
class AnalysisEngine:
    def __init__(self, threshold):
        """
        threshold: A threshold value (in Watts) above which data is considered anomalous.
        """
        self.threshold = threshold

    def analyze(self, data_history):
        """
        Analyze historical data to detect power consumption anomalies.
        Returns a list of data points that exceed the threshold.
        """
        alerts = []
        for data in data_history:
            if data > self.threshold:
                alerts.append(data)
        return alerts

    def generate_trend_report(self, data_history):
        """
        Generate a simple trend report, e.g., the average power consumption.
        Returns a string report.
        """
        if not data_history:
            return "No data to generate report."
        average = sum(data_history) / len(data_history)
        return f"Trend Report: Average power consumption = {average:.2f} Watts"
