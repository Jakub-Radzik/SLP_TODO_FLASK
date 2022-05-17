import hashlib
from flask import request, jsonify, Blueprint, render_template, session, redirect, url_for
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from src.DB.DB import Database

users = Blueprint('users', __name__, template_folder='templates')


@users.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_user = dict(request.form)
        # validate user here
        new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest()
        doc = Database.find_one('users', {"username": new_user["username"]})
        if not doc:
            Database.insert_one('users', new_user)
            print("GITARA")
            return redirect(url_for('users.login'))
        else:
            print("user exists")
    return render_template('register.html')


@users.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_details = dict(request.form)
        user_from_db = Database.find_one('users', {'username': login_details['login']})
        if not user_from_db:
            user_from_db = Database.find_one('users', {'email': login_details['login']})
        if user_from_db:
            encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
            if encrpted_password == user_from_db['password']:
                nickname = user_from_db['username']
                access_token = create_access_token(identity=nickname)
                session['secret_key'] = access_token
                session['username'] = nickname
                print("gitara")
                return redirect(url_for('tasks.get_tasks'))
        print("ERROR")
    return render_template('login.html')


@users.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('users.login'))


@users.route('/settings', methods=['GET', 'POST'])
def settings():
    current_user = session.get('username')
    user_from_db = Database.find_one('users', {'username': current_user})
    if request.method == 'POST':
        pass

    return render_template('settings.html', user=user_from_db)


@users.route("/delete", methods=["POST"])
def delete_user():
    current_user = session.get('username')
    user_from_db = Database.find_one('users', {'username': current_user})
    if user_from_db:
        Database.delete_one('users', {'username': current_user})
        Database.delete_many('tasks', {'username': current_user})
        return redirect(url_for('users.logout'))
    else:
        return redirect(url_for('users.settings'))
