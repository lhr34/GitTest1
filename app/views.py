# app/views.py
from flask import render_template, request, redirect, url_for
from app import app
from app.sensors import PowerSensorSimulator
from app.monitoring import DataProvider, DashboardDisplay, DataLogger
from app.analysis import AnalysisEngine
from app.control import PowerControlContext, AutoControlStrategy
from datetime import datetime
from app.data_store import append_log, read_logs
from flask import Response
import pandas as pd
from flask import request
import math

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


@app.route("/simulation", methods=["GET", "POST"])
def simulation():
    last_data = data_provider.data_history[-1] if data_provider.data_history else None
    new_reading = last_data if last_data else "N/A"
    if request.method == "POST":
        # 获取完整的传感器数据
        sensor_data = sensor.read_value()
        data_provider.set_data(sensor_data)

        append_log(sensor_data, building="Main Library")  # 加入存储

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


@app.route("/logs")  # 新增路由 /logs 页面显示历史记录（支持导出）
def logs():  # 更新 /logs 路由逻辑，添加筛选和分页
    all_logs = read_logs()

    # 提取查询参数
    building_filter = request.args.get('building')
    date_filter = request.args.get('date')
    page = int(request.args.get('page', 1))
    per_page = 10

    # 筛选逻辑
    if building_filter:
        all_logs = [log for log in all_logs if log["building"] == building_filter]

    if date_filter:
        all_logs = [log for log in all_logs if log["timestamp"].startswith(date_filter)]

    # 分页逻辑
    total = len(all_logs)
    total_pages = math.ceil(total / per_page)
    logs_paginated = all_logs[(page - 1) * per_page: page * per_page]

    # 提取唯一建筑列表用于筛选下拉框
    building_options = sorted(set(log['building'] for log in read_logs()))

    return render_template(
        "logs.html",
        title="Power Logs",
        logs=logs_paginated,
        page=page,
        total_pages=total_pages,
        building_filter=building_filter,
        date_filter=date_filter,
        building_options=building_options
    )


@app.route("/export_csv")  # 新增导出功能
def export_csv():
    logs = read_logs()
    df = pd.DataFrame(logs)
    csv_data = df.to_csv(index=False)

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=power_logs.csv"}
    )
