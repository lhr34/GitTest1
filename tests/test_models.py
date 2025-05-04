import pytest
from app.models import User, db


def test_user_creation(app):
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        retrieved = User.query.first()
        assert retrieved.username == 'testuser'
        assert retrieved.email == 'test@example.com'
        assert retrieved.check_password('password')


def test_user_password_hashing():
    user = User(username='testuser')
    user.set_password('correct_password')
    assert user.check_password('correct_password') is True
    assert user.check_password('wrong_password') is False