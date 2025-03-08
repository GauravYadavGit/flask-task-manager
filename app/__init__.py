from flask import Flask, jsonify
from app.database import db
from app.routes import task_bp  # Importing API Routes
from flask_jwt_extended import JWTManager
from app.auth import auth_bp
import os 
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)  # Initialize Flask App

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    db.init_app(app)  # Initialize Database
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()  # Create Tables

    app.register_blueprint(task_bp, url_prefix="/tasks")  # Register Routes
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to the Task Manager API! Use /auth and /tasks."})


    return app
