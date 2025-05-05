# app/analysis.py
"""
Analysis module for power monitoring system.
This module contains the AnalysisEngine class which provides methods for
analyzing power consumption data, generating insights, and detecting anomalies.
"""
import statistics
from datetime import datetime
import numpy as np
from typing import List, Dict, Union, Tuple, Optional


class AnalysisEngine:
    def __init__(self, threshold: float):
        """
        Initialize the Analysis Engine with a threshold for anomaly detection.

        Args:
            threshold (float): A threshold value (in Watts) above which data is considered anomalous.
        """
        self.threshold = threshold
        # Define severity levels as percentages above threshold
        self.severity_levels = {
            'critical': 0.8,  # 80% above threshold
            'high': 0.5,  # 50% above threshold
            'moderate': 0.2,  # 20% above threshold
            'low': 0.0  # At or just above threshold
        }

    def analyze(self, power_history: List[float]) -> List[float]:
        """
        Analyze power history data and return values that exceed the threshold.

        Args:
            power_history (List[float]): A list of power consumption values in Watts.

        Returns:
            List[float]: A list of values that exceed the defined threshold.
        """
        if not power_history:
            return []

        alerts = []
        for data in power_history:
            if data > self.threshold:
                alerts.append(data)
        return alerts

    def analyze_with_severity(self, power_history: List[float]) -> List[Dict[str, Union[float, str]]]:
        """
        Analyze power history data and return values that exceed the threshold with severity levels.

        Args:
            power_history (List[float]): A list of power consumption values in Watts.

        Returns:
            List[Dict]: A list of dictionaries containing the power value and severity level.
        """
        if not power_history:
            return []

        result = []
        for data in power_history:
            if data > self.threshold:
                # Calculate how much it exceeds the threshold by
                excess_percentage = (data - self.threshold) / self.threshold

                # Determine severity based on how much it exceeds the threshold
                # MODIFIED: Changed the logic to correctly assign severity levels
                # The issue was that we were using the first level that matched the condition
                # but we need to find the most severe level that applies
                severity = 'low'  # Default severity
                for level, percentage in sorted(self.severity_levels.items(),
                                                key=lambda x: x[1], reverse=True):
                    if excess_percentage >= percentage:
                        severity = level
                        break

                result.append({
                    'value': data,
                    'severity': severity,
                    'excess_percentage': round(excess_percentage * 100, 2)
                })

        return result

    def generate_trend_report(self, power_history: List[float]) -> str:
        """
        Generate a trend report based on power history data.

        Args:
            power_history (List[float]): A list of power consumption values in Watts.

        Returns:
            str: A report string containing information about power consumption trends.
        """
        if not power_history:
            return "No data to generate report."

        average = sum(power_history) / len(power_history)
        return f"Trend Report: Average power consumption = {average:.2f} Watts"

    def generate_detailed_report(self, power_history: List[float],
                                 timestamps: Optional[List[str]] = None) -> Dict[str, Union[float, str, List]]:
        """
        Generate a detailed report with statistics on power consumption.

        Args:
            power_history (List[float]): A list of power consumption values in Watts.
            timestamps (List[str], optional): A list of timestamps corresponding to power values.

        Returns:
            Dict: A dictionary containing various statistics about power consumption.
        """
        if not power_history:
            return {"status": "No data to generate report."}

        # Calculate basic statistics
        report = {}
        report["average"] = round(sum(power_history) / len(power_history), 2)
        report["min"] = min(power_history)
        report["max"] = max(power_history)

        # Calculate advanced statistics if we have more than one data point
        if len(power_history) > 1:
            report["median"] = statistics.median(power_history)
            report["std_dev"] = round(statistics.stdev(power_history), 2)

        # Count alerts and calculate percentage
        alert_count = sum(1 for x in power_history if x > self.threshold)
        report["alert_percentage"] = round((alert_count / len(power_history)) * 100, 2)

        # Identify trend direction by comparing first third to last third
        if len(power_history) >= 3:
            first_third = sum(power_history[:len(power_history) // 3]) / (len(power_history) // 3)
            last_third = sum(power_history[-len(power_history) // 3:]) / (len(power_history) // 3)

            if last_third > first_third * 1.1:
                report["trend"] = "increasing"
            elif last_third < first_third * 0.9:
                report["trend"] = "decreasing"
            else:
                report["trend"] = "stable"

            report["trend_change_percentage"] = round(((last_third - first_third) / first_third) * 100, 2)

        # Find peak times if timestamps are provided
        if timestamps and len(timestamps) == len(power_history):
            peak_index = power_history.index(max(power_history))
            peak_time = timestamps[peak_index]
            try:
                # Try to parse the timestamp to extract hour information
                peak_datetime = datetime.fromisoformat(peak_time)
                report["peak_hour"] = peak_datetime.hour
            except (ValueError, TypeError):
                # If timestamp format isn't compatible, just store the raw timestamp
                report["peak_time"] = peak_time

        return report

    def detect_patterns(self, power_history: List[float], window_size: int = 5) -> Dict[str, any]:
        """
        Detect patterns in power consumption data such as periodic spikes or consistent increases.

        Args:
            power_history (List[float]): A list of power consumption values in Watts.
            window_size (int): Size of the window to use for moving averages.

        Returns:
            Dict: A dictionary with detected patterns.
        """
        # Need sufficient data for meaningful pattern detection
        if len(power_history) < window_size * 2:
            return {"status": "Insufficient data for pattern detection"}

        results = {}

        # Calculate moving average to smooth out noise
        moving_avgs = []
        for i in range(len(power_history) - window_size + 1):
            window = power_history[i:i + window_size]
            moving_avgs.append(sum(window) / window_size)

        # Check for consistent increase/decrease trends
        increases = sum(1 for i in range(1, len(moving_avgs)) if moving_avgs[i] > moving_avgs[i - 1])
        decreases = sum(1 for i in range(1, len(moving_avgs)) if moving_avgs[i] < moving_avgs[i - 1])

        if increases > len(moving_avgs) * 0.7:
            results["trend_pattern"] = "consistent_increase"
        elif decreases > len(moving_avgs) * 0.7:
            results["trend_pattern"] = "consistent_decrease"
        else:
            results["trend_pattern"] = "fluctuating"

        # Check for cyclic patterns (simple approach: look for alternating increases and decreases)
        alt_count = sum(1 for i in range(2, len(moving_avgs))
                        if (moving_avgs[i] > moving_avgs[i - 1] and moving_avgs[i - 1] < moving_avgs[i - 2]) or
                        (moving_avgs[i] < moving_avgs[i - 1] and moving_avgs[i - 1] > moving_avgs[i - 2]))

        if alt_count > len(moving_avgs) * 0.4:
            results["cyclic_pattern"] = True

        # Count number of spikes (values significantly higher than neighbors)
        spikes = 0
        for i in range(1, len(power_history) - 1):
            if (power_history[i] > power_history[i - 1] * 1.5 and
                    power_history[i] > power_history[i + 1] * 1.5):
                spikes += 1

        results["spike_count"] = spikes

        return results

    def forecast_consumption(self, power_history: List[float], periods_ahead: int = 3) -> List[float]:
        """
        Generate a simple forecast of future power consumption based on historical data.
        Uses a weighted moving average approach where recent values have higher weight.

        Args:
            power_history (List[float]): A list of power consumption values in Watts.
            periods_ahead (int): Number of periods to forecast.

        Returns:
            List[float]: Forecasted power consumption values.
        """
        if len(power_history) < 5:
            # Not enough data for meaningful forecast, use simple average
            return [sum(power_history) / len(power_history)] * periods_ahead

        forecast = []

        # Simple weighted moving average where recent values have higher weights
        weights = [0.1, 0.15, 0.2, 0.25, 0.3]  # Weights for last 5 values (most recent last)

        for _ in range(periods_ahead):
            last_values = power_history[-5:]

            # If we don't have 5 values yet, adjust weights proportionally
            if len(last_values) < 5:
                adjusted_weights = weights[-len(last_values):]
                adjusted_weights = [w / sum(adjusted_weights) for w in adjusted_weights]
                prediction = sum(v * w for v, w in zip(last_values, adjusted_weights))
            else:
                prediction = sum(v * w for v, w in zip(last_values, weights))

            forecast.append(round(prediction, 2))
            power_history.append(prediction)  # Add prediction to history for next iteration

        return forecast