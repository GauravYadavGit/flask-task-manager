from flask import Blueprint, request, jsonify
from app.models import Task
from app.database import db

task_bp = Blueprint("tasks", __name__)  # Creating a blueprint for tasks


# ✅ GET and POST tasks
@task_bp.route("/", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        tasks = Task.query.all()
        return jsonify(
            [
                {"id": task.id, "title": task.title, "completed": task.completed}
                for task in tasks
            ]
        )

    if request.method == "POST":
        data = request.get_json()
        new_task = Task(
            title=data["title"],
            description=data.get("description", ""),
            completed=False,
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": "Task created", "id": new_task.id}), 201


# ✅ PATCH: Update task status
@task_bp.route("/<int:task_id>/status", methods=["PATCH"])
def update_task_status(task_id):
    task = db.session.get(Task, task_id)  # ✅ New Method
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task.completed = data.get("completed", task.completed)
    db.session.commit()
    return jsonify({"message": "Task status updated"})


# ✅ DELETE: Remove a task
@task_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = db.session.get(Task, task_id)  # ✅ Use session.get()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})
