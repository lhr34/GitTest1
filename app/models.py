
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# User model for authentication and authorization
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # Unique ID for each user
    id = db.Column(db.Integer, primary_key=True)

    # Username must be unique and indexed for fast lookup
    username = db.Column(db.String(64), unique=True, index=True)

    # Email must be unique and indexed
    email = db.Column(db.String(120), unique=True, index=True)

    # Hashed password (not stored in plain text)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        # Store the securely hashed version of the password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Compare input password with stored hash
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        # Developer-friendly string representation
        return f'<User {self.username}>'

# Flask-Login loader function to reload a user from the session
@login.user_loader
def load_user(user_id):
    # Convert user_id back to an integer and query the database
    return User.query.get(int(user_id))
