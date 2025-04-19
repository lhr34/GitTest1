# app/views.py
from flask import render_template, request, redirect, url_for
from app import app
from app.sensors import PowerSensorSimulator
from app.monitoring import DataProvider, DashboardDisplay, DataLogger
from app.analysis import AnalysisEngine
from app.control import PowerControlContext, AutoControlStrategy
from datetime import datetime

# Initialize global simulation objects
sensor = PowerSensorSimulator()
data_provider = DataProvider()
dashboard = DashboardDisplay()
data_logger = DataLogger()

# Subscribe observers to the DataProvider
data_provider.subscribe(dashboard)
data_provider.subscribe(data_logger)

# Initialize the AnalysisEngine with a threshold of 450 Watts
analysis_engine = AnalysisEngine(threshold=450)

# Initialize the control context with auto control strategy (threshold = 420 Watts)
auto_strategy = AutoControlStrategy()
control_context = PowerControlContext(strategy=auto_strategy)


@app.route("/")
def home():
    return render_template("home.html", title="Home")


# app/views.py
@app.route("/simulation", methods=["GET", "POST"])
def simulation():
    last_data = data_provider.data_history[-1] if data_provider.data_history else None
    new_reading = last_data if last_data else "N/A"
    if request.method == "POST":
        # 获取完整的传感器数据
        sensor_data = sensor.read_value()
        data_provider.set_data(sensor_data)
        # 执行控制策略
        control_action = control_context.execute_control(sensor_data)
    else:
        control_action = "N/A"

    # 生成分析报告
    power_history = [d['PowerSensor'] for d in data_provider.data_history]
    alerts = analysis_engine.analyze(power_history)
    report = analysis_engine.generate_trend_report(power_history)
    timestamps = [d['timestamp'] for d in data_provider.data_history]

    return render_template("simulation.html",
                           title="Simulation",
                           latest_reading=new_reading,
                           control_action=control_action,
                           power_history=power_history,  # 保持向后兼容
                           alerts=alerts,
                           report=report,
                           timestamps=timestamps
                           )


@app.route("/reset_simulation", methods=["POST"])
def reset_simulation():
    data_provider.data_history.clear()
    return redirect(url_for("simulation"))
