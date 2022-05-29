from datetime import datetime

from bson import ObjectId
from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.DB.DB import Database

tasks = Blueprint('tasks', __name__)
default_msg = "It's me! Message box."


@tasks.route("/tasks", methods=["GET"])
def get_tasks():
    current_user = session.get('username')
    print(current_user)
    user_from_db = Database.find_one('users', {'username': current_user})
    if user_from_db:
        tasks_from_db = Database.find('tasks', {'user_id': str(user_from_db['_id'])})
        tasks = []
        for task in tasks_from_db:
            task['_id'] = str(task['_id'])
            tasks.append(task)
        try:
            progress = int(100 * (sum(1 if task['completed'] else 0 for task in tasks) / len(tasks)))
        except ZeroDivisionError:
            progress = 0
        return render_template('tasks.html', tasks=tasks, progress=progress, msg=default_msg)
    else:
        return redirect(url_for('users.login'))


@tasks.route("/create", methods=["GET", "POST"])
def create_task():
    current_user = session.get('username')
    user_from_db = Database.find_one('users', {'username': current_user})
    if not user_from_db:
        return redirect(url_for('users.login'))
    if request.method == "POST":
        new_task = dict(request.form)
        new_task['user_id'] = str(user_from_db['_id'])
        new_task['completed'] = False
        new_task['created_at'] = str(datetime.now())
        Database.insert_one('tasks', new_task)
        return redirect(url_for('tasks.get_tasks'))
    else:
        return render_template('create_task.html')


@tasks.route("/tasks/<task_id>", methods=["GET"])
def delete_task(task_id):
    current_user = session.get('username')
    user_from_db = Database.find_one('users', {'username': current_user})
    if user_from_db:
        Database.delete_one('tasks', {'_id': ObjectId(task_id)})
        return redirect(url_for('tasks.get_tasks'))


@tasks.route("/tasks/duplicate/<task_id>", methods=["GET"])
def duplicate_task(task_id):
    current_user = session.get('username')
    user_from_db = Database.find_one('users', {'username': current_user})
    if user_from_db:
        finded = Database.find_one('tasks', {'_id': ObjectId(task_id)})
        if finded:
            del finded['_id']
            finded['created_at'] = str(datetime.now())
            try:
                del finded['modified_at']
            except:
                pass
            Database.insert_one('tasks', finded)
    return redirect(url_for('tasks.get_tasks'))


@tasks.route("/tasks/<task_id>", methods=["GET"])
@jwt_required()
def get_task_by_id(task_id):
    current_user = get_jwt_identity()
    user_from_db = Database.find_one('users', {'username': current_user})
    if user_from_db:
        task = Database.find_one('tasks', ObjectId(task_id))
        if task:
            del task['_id']
            del task['user_id']
            return jsonify({'task': task}), 200
        else:
            return jsonify({'msg': 'Task not found'}), 404
    else:
        return jsonify({'msg': 'Profile not found'}), 404


@tasks.route("/update/<task_id>", methods=["GET", "POST"])
def update_task(task_id):
    current_user = session.get('username')
    user_from_db = Database.find_one('users', {'username': current_user})
    if not user_from_db:
        return redirect(url_for('users.login'))
    task = Database.find_one('tasks', ObjectId(task_id))
    if request.method == "POST":
        if task:
            task_data = dict(request.form)
            task_data['user_id'] = str(user_from_db['_id'])
            task_data['modified_at'] = str(datetime.now())
            Database.update_one('tasks', {'_id': ObjectId(task_id)}, {'$set': task_data})
            return redirect(url_for('tasks.get_tasks'))
    else:
        return render_template('update_task.html', task=task)


@tasks.route("/toggle_status/<task_id>", methods=['GET'])
def toggle_status(task_id):
    current_user = session.get('username')
    user_from_db = Database.find_one('users', {'username': current_user})
    if not user_from_db:
        return redirect(url_for('users.login'))
    task = Database.find_one('tasks', ObjectId(task_id))
    if task:
        task['completed'] = not task['completed']
        Database.update_one('tasks', {'_id': ObjectId(task_id)}, {'$set': task})
    return redirect(url_for('tasks.get_tasks'))
