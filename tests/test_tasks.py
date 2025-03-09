import pytest
from app import create_app
from app.database import db
from app.models import Task

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

def test_create_task(client):
    """Test task creation"""
    response = client.post("/tasks/", json={"title": "Test Task", "description": "This is a test task"})
    assert response.status_code == 201
    assert "Task created" in response.get_json()["message"]

def test_get_tasks(client):
    """Test fetching tasks"""
    client.post("/tasks/", json={"title": "Test Task", "description": "This is a test task"})
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_update_task_status(client):
    """Test updating task status"""
    client.post("/tasks/", json={"title": "Test Task", "description": "This is a test task"})
    response = client.patch("/tasks/1/status", json={"completed": True})
    assert response.status_code == 200
    assert "Task status updated" in response.get_json()["message"]

def test_delete_task(client):
    """Test deleting a task"""
    client.post("/tasks/", json={"title": "Test Task", "description": "This is a test task"})
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert "Task deleted" in response.get_json()["message"]
