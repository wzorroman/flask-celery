import logging

from celery.result import AsyncResult
from flask import render_template, jsonify, request

from project.server.tasks import create_task

from . import main_blueprint

logger = logging.getLogger(__name__)


@main_blueprint.route("/", methods=["GET"])
def home():
    return render_template("main/home.html")

@main_blueprint.route("/hello", methods=["GET"])
def hello_world():
    return '''
        <!doctype html>
        <title>Celery - Flask</title>
        <h1>Welcome to project Flask - Celery</h1>
    '''

@main_blueprint.route("/tasks", methods=["POST"])
def run_task():
    content = request.json
    task_type = content["type"]
    task = create_task.delay(int(task_type))
    return jsonify({"task_id": task.id}), 202


@main_blueprint.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return jsonify(result), 200
