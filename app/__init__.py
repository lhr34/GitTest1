# app/__init__.py
from flask import Flask
from config import Config
from jinja2 import StrictUndefined
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.config.from_object(Config)
db = SQLAlchemy(app)

# 初始化 LoginManager 以支持用户认证
login = LoginManager(app)
login.login_view = 'login'

# 导入模块（注意：models.py 中需要包含 user_loader 回调）
from app import views, models, debug_utils

@app.shell_context_processor
def make_shell_context():
    return dict(db=db)
