# app/views.py
from flask import render_template, request, redirect, url_for
from app import app
from app.sensors import PowerSensorSimulator
from app.monitoring import DataProvider, DashboardDisplay, DataLogger
from app.analysis import AnalysisEngine
from app.control import PowerControlContext, AutoControlStrategy, ManualControlStrategy

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
auto_strategy = AutoControlStrategy(control_threshold=420)
control_context = PowerControlContext(strategy=auto_strategy)


@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/simulation", methods=["GET", "POST"])
def simulation():
    if request.method == "POST":
        # Simulate a new sensor reading
        new_reading = sensor.read_value()
        data_provider.set_data(new_reading)
        # Execute the control strategy based on the new reading
        control_action = control_context.execute_control(new_reading)
    else:
        # For GET requests, show last reading if available
        new_reading = data_provider.data_history[-1] if data_provider.data_history else "N/A"
        control_action = "N/A"

    # Generate analysis report based on current data history
    alerts = analysis_engine.analyze(data_provider.data_history)
    report = analysis_engine.generate_trend_report(data_provider.data_history)

    return render_template("simulation.html",
                           title="Simulation",
                           latest_reading=new_reading,
                           control_action=control_action,
                           data_history=data_provider.data_history,
                           alerts=alerts,
                           report=report)


@app.route("/reset_simulation", methods=["POST"])
def reset_simulation_route():
    data_provider.data_history.clear()
    return redirect(url_for("simulation"))
