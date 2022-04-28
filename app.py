import datetime

from flask import Flask, redirect, url_for, session
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.API.tasks import tasks
from src.API.users import users
from flask_pymongo import PyMongo

from src.DB.DB import Database


def create_app():
    app = Flask(__name__)
    Database.init()
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/slp_todo'
    mongo = PyMongo(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.secret_key = "super secret key"
    jwt = JWTManager(app)
    app.config['JWT_SECRET_KEY'] = '5369656D696E736B69546F4A6562616E794377656C4B757277794E6965436863655A6E61634C4D414F'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=2)
    register_blueprints(app)

    @app.route('/')
    def hello_world():
        return redirect(url_for('users.login'))

    return app


def register_blueprints(app):
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(tasks, url_prefix='/tasks')


if __name__ == '__main__':
    create_app().run(debug=True, use_reloader=True)
