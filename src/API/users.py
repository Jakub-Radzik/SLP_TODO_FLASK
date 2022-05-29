import hashlib

from bson import ObjectId
from flask import request, Blueprint, render_template, session, redirect, url_for
from flask_jwt_extended import create_access_token

from src.DB.DB import Database

users = Blueprint('users', __name__, template_folder='templates')
default_msg = "It's me! Message box."


@users.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_user = dict(request.form)
        if new_user["password"] == new_user["repeat_password"]:
            del new_user["repeat_password"]
            new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest()
            doc = Database.find_one('users', {"username": new_user["username"]})
            if not doc:
                Database.insert_one('users', new_user)
                return redirect(url_for('users.login'))
            else:
                return render_template('register.html', msg="User exist !!!")
        else:
            return render_template('register.html', msg="Passwords are different !!!")
    return render_template('register.html', msg=default_msg)


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
        return render_template('login.html', msg="Something went wrong with logging into system.")
    return render_template('login.html', msg=default_msg)


@users.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('users.login'))


# include password change
@users.route('/settings', methods=['GET', 'POST'])
def settings():
    current_user = session.get('username')
    user_from_db = Database.find_one('users', {'username': current_user})
    if request.method == 'POST':
        details = dict(request.form)
        if details['password'] == details['repeat_password'] and hashlib.sha256(
                details['old_password'].encode("utf-8")).hexdigest() == user_from_db['password']:
            user_from_db['password'] = hashlib.sha256(details['password'].encode("utf-8")).hexdigest()
            Database.update_one('users', {'_id': ObjectId(user_from_db['_id'])}, {'$set': user_from_db})
            return render_template('settings.html', user=user_from_db, msg="Passoword correctly changed")
        else:
            return render_template('settings.html', user=user_from_db, msg="Something went wrong with your new passwords!!!")
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
