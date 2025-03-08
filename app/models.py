from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Task(db.Model):  # Inherit from SQLAlchemy Model
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing Task ID
    title = db.Column(db.String(100), nullable=False)  # Task title
    description = db.Column(db.String(255), nullable=True)  # Task details
    completed = db.Column(db.Boolean, default=False)  # Task completion status


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)    
