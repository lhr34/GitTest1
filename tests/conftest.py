"""
Test configuration and fixtures for Flask app:
- Creates test app with in-memory SQLite database
- Manages database schema setup/teardown
- Provides test client for endpoint testing
"""

import pytest
from app import create_app, db

# This fixture sets up a temporary Flask app for testing
@pytest.fixture
def app():
    # Create the Flask app using your factory pattern
    app = create_app()

    # Override the default config with test-specific settings
    app.config.update({
        "TESTING": True,  # Enables test mode
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use in-memory database for tests
        "SQLALCHEMY_TRACK_MODIFICATIONS": False  # Disable the event system to save resources
    })

    # Establish an application context so we can work with the database
    with app.app_context():
        db.create_all()  # Create all database tables before the test
        yield app        # This is where the testing happens
        db.drop_all()    # Clean up after the test by dropping all tables

# This fixture provides a test client that can simulate HTTP requests to your app
@pytest.fixture
def client(app):
    return app.test_client()  # Return a test client bound to the app fixturern app.test_client()