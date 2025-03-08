from flask import Flask
from app.database import db
from app.routes import task_bp  # Importing API Routes

def create_app():
    app = Flask(__name__)  # Initialize Flask App

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)  # Initialize Database

    with app.app_context():
        db.create_all()  # Create Tables

    app.register_blueprint(task_bp, url_prefix="/tasks")  # Register Routes

    return app
