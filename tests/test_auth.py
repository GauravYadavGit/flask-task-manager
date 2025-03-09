import pytest
from app import create_app
from app.database import db
from app.models import User

@pytest.fixture
def client():
    """Set up a test client"""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # In-memory DB
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_user_registration(client):
    """Test user registration"""
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpass"
    })
    
    print("Response JSON:", response.get_json())  # 🔍 Debugging
    
    assert response.status_code == 201
    assert "User registered successfully" in response.get_json()["message"]


def test_user_login(client):
    """Test user login"""
    # Register user
    client.post("/auth/register", json={"username": "testuser", "password": "testpass"})
    # Login user
    response = client.post("/auth/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.get_json()
