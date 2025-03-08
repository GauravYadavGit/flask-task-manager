from flask import Blueprint, request, jsonify
from app.models import Task
from app.database import db

task_bp = Blueprint("tasks", __name__)  # Creating a blueprint for tasks

@task_bp.route("/", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()  # Fetch all tasks from the DB
    return jsonify([{"id": task.id, "title": task.title, "completed": task.completed} for task in tasks])
