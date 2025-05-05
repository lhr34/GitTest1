"""
User Model Tests:
- Database persistence and retrieval
- Password hashing/verification security
"""

import pytest
from app.models import User, db

# Test creating a user and saving it to the database
def test_user_creation(app):
    with app.app_context():
        # Create and add a new user to the DB
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        # Query the user back
        retrieved = User.query.first()
        assert retrieved.username == 'testuser'
        assert retrieved.email == 'test@example.com'
        assert retrieved.check_password('password')  # Confirm password hashing works

# Test password hashing and verification independently of the DB
def test_user_password_hashing():
    user = User(username='testuser')
    user.set_password('correct_password')

    # Correct password should return True
    assert user.check_password('correct_password') is True

    # Incorrect password should return False
    assert user.check_password('wrong_password') is False
