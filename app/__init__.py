from flask import Flask
from config import Config
from jinja2 import StrictUndefined
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from app.control_model import train_power_model
from app.monitoring import DataProvider


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.config.from_object(Config)
db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'
data_provider = DataProvider()


from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    db.init_app(app)
    with app.app_context():
        from app import models

    return app

# training RF Model when first running the app
def auto_train_model():
    model_dir = "app/ML_Model"
    model_path = os.path.join(model_dir, "rf_power_model.pkl")
    encoder_path = os.path.join(model_dir, "label_encoder.pkl")

    # check if the model already exists
    if not os.path.exists(model_path) or not os.path.exists(encoder_path):
        print("Starting automatic model training...")
        try:
            os.makedirs(model_dir, exist_ok=True)

            model, le = train_power_model()
            print("Model training completed successfully")

        except Exception as e:
            print(f"Model training failed: {str(e)}")
    else:
        print("Found existing model files, skipping training")

with app.app_context():
    auto_train_model()

# other imports
from app import views, models, debug_utils


@app.shell_context_processor
def make_shell_context():
    return dict(db=db)