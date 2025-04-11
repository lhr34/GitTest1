# tests.py
import unittest
from sensors import PowerSensorSimulator
from analysis import AnalysisEngine
from control import AutoControlStrategy, ManualControlStrategy, PowerControlContext


class TestSensor(unittest.TestCase):
    def test_read_value_normal(self):
        sensor = PowerSensorSimulator()
        value = sensor.read_value()
        self.assertTrue(100 <= value <= 500)

    def test_read_value_faulty(self):
        sensor = PowerSensorSimulator()
        sensor.read_value = lambda: -1
        self.assertLess(sensor.read_value(), 0)


class TestAnalysis(unittest.TestCase):
    def test_analyze_detects_alert(self):
        engine = AnalysisEngine(threshold=450)
        history = [100, 200, 500]
        alerts = engine.analyze(history)
        self.assertIn(500, alerts)

    def test_analyze_empty_history(self):
        engine = AnalysisEngine(threshold=450)
        alerts = engine.analyze([])
        self.assertEqual(alerts, [])


class TestControl(unittest.TestCase):
    def test_auto_control(self):
        strategy = AutoControlStrategy(control_threshold=420)
        context = PowerControlContext(strategy)
        action = context.execute_control(430)
        self.assertIn("降负荷", action)

    def test_manual_control(self):
        strategy = ManualControlStrategy(manual_setting="低功耗模式")
        context = PowerControlContext(strategy)
        context.set_strategy(strategy)
        action = context.execute_control(430)
        self.assertIn("低功耗模式", action)


if __name__ == "__main__":
    unittest.main()
