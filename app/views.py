from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app
from app.sensors import PowerSensorSimulator
from app.monitoring import DataProvider, DashboardDisplay, DataLogger
from app.analysis import AnalysisEngine
from app.control import PowerControlContext, AutoControlStrategy, ManualControlStrategy, SimpleControlSystem, \
    SimpleControlAdapter
from datetime import datetime
from app.data_store import append_log, read_logs
from flask import Response
import pandas as pd
from flask import request, session
import math

# Initialize system components
sensor = PowerSensorSimulator()
data_provider = DataProvider()
dashboard = DashboardDisplay()
data_logger = DataLogger()

# Set up the observer pattern for monitoring
data_provider.subscribe(dashboard)
data_provider.subscribe(data_logger)

# Initialize analysis engine with threshold value for alerts
analysis_engine = AnalysisEngine(threshold=450)

# Initialize control system strategies
auto_strategy = AutoControlStrategy()
manual_strategy = ManualControlStrategy()
control_context = PowerControlContext(strategy=auto_strategy)

# Initialize simple control system and its adapter
simple_system = SimpleControlSystem()
simple_adapter = SimpleControlAdapter(simple_system)


@app.route("/")
def home():
    """Home page route"""
    return render_template("home.html", title="Home")


@app.route("/simulation", methods=["GET", "POST"])
def simulation():
    """
    Simulation page route - handles power control, sensor data simulation,
    and provides analytics for the dashboard
    """
    # Get the latest reading if available
    last_data = data_provider.data_history[-1] if data_provider.data_history else None
    new_reading = last_data if last_data else "N/A"

    # Get current control mode from session
    control_mode = session.get('control_mode', 'auto')

    # Handle POST requests (form submissions and simulation actions)
    if request.method == "POST":
        # Handle control mode changes
        if 'control_mode' in request.form:
            mode = request.form['control_mode']
            if mode == 'auto':
                control_context.set_strategy(auto_strategy)
                session['control_mode'] = 'auto'
                flash('Switched to AUTO control mode')
            elif mode == 'simple':
                control_context.set_strategy(simple_adapter)
                session['control_mode'] = 'simple'
                flash('Switched to SIMPLE control system')
            else:
                manual_strategy.set_mode(mode)
                control_context.set_strategy(manual_strategy)
                session['control_mode'] = mode
                flash(f'Switched to MANUAL control - {mode.upper()} mode')
            return redirect(url_for('simulation'))

        # Generate new sensor reading and log it
        sensor_data = sensor.read_value()
        data_provider.set_data(sensor_data)
        append_log(sensor_data, building="Main Library")

        # Execute control action based on new reading
        control_action = control_context.execute_control(sensor_data)
    else:
        # For GET requests, use existing data if available
        if new_reading != "N/A":
            control_action = control_context.execute_control(new_reading)
        else:
            control_action = "No data available"

    # Extract power history and timestamps for analysis
    power_history = [d['PowerSensor'] for d in data_provider.data_history]
    timestamps = [d['timestamp'] for d in data_provider.data_history]

    # Basic analysis (original functionality)
    alerts = analysis_engine.analyze(power_history)
    report = analysis_engine.generate_trend_report(power_history)

    # Advanced analysis (new functionality)
    alerts_with_severity = []
    detailed_report = {}
    patterns = {}
    forecast = []

    # Only perform advanced analysis if we have sufficient data
    if len(power_history) > 0:
        # Generate severity-based alerts
        alerts_with_severity = analysis_engine.analyze_with_severity(power_history)

        # Generate detailed statistical report
        detailed_report = analysis_engine.generate_detailed_report(power_history, timestamps)

        # Pattern detection requires more data points
        if len(power_history) >= 10:
            patterns = analysis_engine.detect_patterns(power_history, window_size=5)

        # Generate forecast for future periods
        forecast = analysis_engine.forecast_consumption(power_history.copy(), periods_ahead=3)

    # Render template with all analysis data
    return render_template("simulation.html",
                           title="Simulation",
                           latest_reading=new_reading,
                           control_action=control_action,
                           power_history=power_history,
                           alerts=alerts,
                           report=report,
                           timestamps=timestamps,
                           control_mode=control_mode,
                           # New advanced analytics data
                           alerts_with_severity=alerts_with_severity,
                           detailed_report=detailed_report,
                           patterns=patterns,
                           forecast=forecast,
                           threshold=analysis_engine.threshold)  # Pass threshold value to template


@app.route("/reset_simulation", methods=["POST"])
def reset_simulation():
    """Reset the simulation by clearing all historical data"""
    data_provider.data_history.clear()
    return redirect(url_for("simulation"))


@app.route("/logs")
def logs():
    """
    Logs page route - displays historical power logs with filtering and pagination
    """
    # Get all logs from storage
    all_logs = read_logs()

    # Apply filters if provided in query parameters
    building_filter = request.args.get('building')
    date_filter = request.args.get('date')
    page = int(request.args.get('page', 1))
    per_page = 10  # Items per page

    # Filter by building if specified
    if building_filter:
        all_logs = [log for log in all_logs if log["building"] == building_filter]

    # Filter by date if specified
    if date_filter:
        all_logs = [log for log in all_logs if log["timestamp"].startswith(date_filter)]

    # Calculate pagination values
    total = len(all_logs)
    total_pages = math.ceil(total / per_page)
    logs_paginated = all_logs[(page - 1) * per_page: page * per_page]

    # Get unique building options for the filter dropdown
    building_options = sorted(set(log['building'] for log in read_logs()))

    # Render the logs template with data
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
    """Export logs data as a CSV file for download"""
    logs = read_logs()
    df = pd.DataFrame(logs)
    csv_data = df.to_csv(index=False)

    # Return as a downloadable CSV file
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=power_logs.csv"}
    )


@app.route("/api/analysis", methods=["GET"])
def api_analysis():
    """
    API endpoint to provide analysis data in JSON format
    Used for asynchronous updating of analysis panels in the dashboard
    """
    # Get power history and timestamps
    power_history = [d['PowerSensor'] for d in data_provider.data_history]
    timestamps = [d['timestamp'] for d in data_provider.data_history]

    # Return error if no data is available
    if not power_history:
        return jsonify({"error": "No data available"})

    # Perform various analyses
    alerts = analysis_engine.analyze(power_history)
    alerts_with_severity = analysis_engine.analyze_with_severity(power_history)
    detailed_report = analysis_engine.generate_detailed_report(power_history, timestamps)

    # Only perform pattern detection and forecasting with sufficient data
    patterns = {}
    forecast = []
    if len(power_history) >= 10:
        patterns = analysis_engine.detect_patterns(power_history)
        forecast = analysis_engine.forecast_consumption(power_history.copy(), periods_ahead=3)

    # Return all analysis results as JSON
    return jsonify({
        "basic_report": analysis_engine.generate_trend_report(power_history),
        "alerts": alerts,
        "alerts_with_severity": alerts_with_severity,
        "detailed_report": detailed_report,
        "patterns": patterns,
        "forecast": forecast
    })