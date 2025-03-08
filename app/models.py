from app.database import db

class Task(db.Model):  # Inherit from SQLAlchemy Model
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing Task ID
    title = db.Column(db.String(100), nullable=False)  # Task title
    description = db.Column(db.String(255), nullable=True)  # Task details
    completed = db.Column(db.Boolean, default=False)  # Task completion status
