import datetime
from flask import Flask, redirect, url_for, session
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.API.tasks import tasks
from src.API.users import users
from src.DB.DB import init_db

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = "super secret key"
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = '5369656D696E736B69546F4A6562616E794377656C4B757277794E6965436863655A6E61634C4D414F'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=2)


def register_blueprints(app):
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(tasks, url_prefix='/tasks')


register_blueprints(app)


@app.route('/')
def hello_world():
    return redirect(url_for('users.login'))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
