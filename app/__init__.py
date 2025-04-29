from flask import Flask
from config import Config
from jinja2 import StrictUndefined
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from app.control_model import train_power_model  # 导入训练函数

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.config.from_object(Config)
db = SQLAlchemy(app)

# 初始化 LoginManager
login = LoginManager(app)
login.login_view = 'login'


# 自动训练模型的逻辑
def auto_train_model():
    model_dir = "app/ML_Model"
    model_path = os.path.join(model_dir, "rf_power_model.pkl")
    encoder_path = os.path.join(model_dir, "label_encoder.pkl")

    # 检查模型是否存在
    if not os.path.exists(model_path) or not os.path.exists(encoder_path):
        print("⏳ Starting automatic model training...")
        try:
            # 创建模型目录
            os.makedirs(model_dir, exist_ok=True)

            # 执行训练流程
            model, le = train_power_model()
            print("✅ Model training completed successfully")

        except Exception as e:
            print(f"❌ Model training failed: {str(e)}")
    else:
        print("🔍 Found existing model files, skipping training")


# 在应用初始化时执行训练
with app.app_context():
    auto_train_model()

# 导入其他模块
from app import views, models, debug_utils


@app.shell_context_processor
def make_shell_context():
    return dict(db=db)