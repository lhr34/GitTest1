from flask import render_template, request, redirect, url_for, flash
from app import app
from app.sensors import PowerSensorSimulator
from app.monitoring import DataProvider, DashboardDisplay, DataLogger
from app.analysis import AnalysisEngine
from app.control import PowerControlContext, AutoControlStrategy, ManualControlStrategy, SimpleControlSystem, SimpleControlAdapter
from datetime import datetime
from app.data_store import append_log, read_logs
from flask import Response
import pandas as pd
from flask import request, session
import math

# Initialize  system
sensor = PowerSensorSimulator()
data_provider = DataProvider()
dashboard = DashboardDisplay()
data_logger = DataLogger()

data_provider.subscribe(dashboard)
data_provider.subscribe(data_logger)

analysis_engine = AnalysisEngine(threshold=450)

# Initialize control system
auto_strategy = AutoControlStrategy()
manual_strategy = ManualControlStrategy()
control_context = PowerControlContext(strategy=auto_strategy)

# Initialize simple control system and its adapter
simple_system = SimpleControlSystem()
simple_adapter = SimpleControlAdapter(simple_system)

@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/simulation", methods=["GET", "POST"])
def simulation():
    last_data = data_provider.data_history[-1] if data_provider.data_history else None
    new_reading = last_data if last_data else "N/A"
    control_mode = session.get('control_mode', 'auto')

    # power control panel
    if request.method == "POST":
        if 'control_mode' in request.form:
            mode = request.form['control_mode']
            if mode == 'auto':
                control_context.set_strategy(auto_strategy)
                session['control_mode'] = 'auto'
                flash('Switched to AUTO control mode')
            elif mode == 'simple':
                control_context.set_strategy(legacy_adapter)
                session['control_mode'] = 'simple'
                flash('Switched to SIMPLE control system')
            else:
                manual_strategy.set_mode(mode)
                control_context.set_strategy(manual_strategy)
                session['control_mode'] = mode
                flash(f'Switched to MANUAL control - {mode.upper()} mode')
            return redirect(url_for('simulation'))

        # get sensor data, set log and display
        sensor_data = sensor.read_value()
        data_provider.set_data(sensor_data)
        append_log(sensor_data, building="Main Library")

        # power control action
        control_action = control_context.execute_control(sensor_data)
    else:
        if new_reading != "N/A":
            control_action = control_context.execute_control(new_reading)
        else:
            control_action = "No data available"

    # Generate analysis report
    power_history = [d['PowerSensor'] for d in data_provider.data_history]
    alerts = analysis_engine.analyze(power_history)
    report = analysis_engine.generate_trend_report(power_history)
    timestamps = [d['timestamp'] for d in data_provider.data_history]

    return render_template("simulation.html",
                           title="Simulation",
                           latest_reading=new_reading,
                           control_action=control_action,
                           power_history=power_history,
                           alerts=alerts,
                           report=report,
                           timestamps=timestamps,
                           control_mode=control_mode)


@app.route("/reset_simulation", methods=["POST"])
def reset_simulation():
    data_provider.data_history.clear()
    return redirect(url_for("simulation"))


@app.route("/logs")
def logs():
    all_logs = read_logs()

    building_filter = request.args.get('building')
    date_filter = request.args.get('date')
    page = int(request.args.get('page', 1))
    per_page = 10

    if building_filter:
        all_logs = [log for log in all_logs if log["building"] == building_filter]

    if date_filter:
        all_logs = [log for log in all_logs if log["timestamp"].startswith(date_filter)]

    total = len(all_logs)
    total_pages = math.ceil(total / per_page)
    logs_paginated = all_logs[(page - 1) * per_page: page * per_page]

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


@app.route("/export_csv")
def export_csv():
    logs = read_logs()
    df = pd.DataFrame(logs)
    csv_data = df.to_csv(index=False)

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=power_logs.csv"}
    )