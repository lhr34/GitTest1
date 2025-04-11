# config.py
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    # 数据库配置（这里使用 SQLite，如无数据库需求可忽略）
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

