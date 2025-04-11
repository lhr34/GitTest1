# app/models.py
from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # 其它字段可以根据需要增加

    def __repr__(self):
        return f'<User {self.username}>'

# Flask-Login user_loader 回调
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
