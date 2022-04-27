from bson import ObjectId
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


tasks = Blueprint('tasks', __name__)


@tasks.route("/api/v1/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    user_from_db = users_collection.find_one({'username': current_user})
    if user_from_db:
        tasks_from_db = tasks_collection.find({'user_id': str(user_from_db['_id'])})
        tasks = []
        for task in tasks_from_db:
            task['_id'] = str(task['_id'])
            tasks.append(task)
        return jsonify({'tasks': tasks}), 200
    else:
        return jsonify({'msg': 'Profile not found'}), 404


@tasks.route("/api/v1/tasks", methods=["POST"])
@jwt_required()
def add_task():
    current_user = get_jwt_identity()
    user_from_db = users_collection.find_one({'username': current_user})
    if user_from_db:
        new_task = request.get_json()
        new_task['user_id'] = str(user_from_db['_id'])
        tasks_collection.insert_one(new_task)
        return jsonify({'msg': 'Task added successfully'}), 201
    else:
        return jsonify({'msg': 'Profile not found'}), 404


@tasks.route("/api/v1/tasks/<task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    current_user = get_jwt_identity()
    user_from_db = users_collection.find_one({'username': current_user})
    if user_from_db:
        tasks_collection.delete_one({'_id': ObjectId(task_id)})
        return jsonify({'msg': 'Task deleted successfully'}), 200
    else:
        return jsonify({'msg': 'Profile not found'}), 404


# todo: change method to PUT
@tasks.route("/api/v1/tasks/duplicate/<task_id>", methods=["GET"])
@jwt_required()
def duplicate_task(task_id):
    current_user = get_jwt_identity()
    user_from_db = users_collection.find_one({'username': current_user})
    if user_from_db:
        finded = tasks_collection.find_one({'_id': ObjectId(task_id)})
        if finded:
            del finded['_id']
            tasks_collection.insert_one(finded)
            return jsonify({'msg': 'Task duplicated successfully'}), 200
        else:
            return jsonify({'msg': 'Task not found'}), 404
    else:
        return jsonify({'msg': 'Profile not found'}), 404


@tasks.route("/api/v1/tasks/<task_id>", methods=["GET"])
@jwt_required()
def get_task_by_id(task_id):
    current_user = get_jwt_identity()
    user_from_db = users_collection.find_one({'username': current_user})
    if user_from_db:
        task = tasks_collection.find_one(ObjectId(task_id))
        if task:
            del task['_id']
            del task['user_id']
            return jsonify({'task': task}), 200
        else:
            return jsonify({'msg': 'Task not found'}), 404
    else:
        return jsonify({'msg': 'Profile not found'}), 404


@tasks.route("/api/v1/tasks/<task_id>", methods=["PATCH"])
@jwt_required()
def update_task(task_id):
    current_user = get_jwt_identity()
    user_from_db = users_collection.find_one({'username': current_user})
    if user_from_db:
        updated_task = request.get_json()
        print(updated_task)
        tasks_collection.update_one({'_id': ObjectId(task_id)}, {'$set': updated_task})
        return jsonify({'msg': 'Task updated successfully'}), 200
    else:
        return jsonify({'msg': 'Profile not found'}), 404