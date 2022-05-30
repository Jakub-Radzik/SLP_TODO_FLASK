import datetime

from flask import Flask, redirect, url_for
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.API.tasks import tasks
from src.API.users import users

from src.DB.DB import Database

app = Flask(__name__)
Database.init()
app.config['MONGO_URI'] = 'mongodb://localhost:27017/slp_todo'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = "super secret key"
jwt = JWTManager(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['JWT_SECRET_KEY'] = '5369656D696E736B69546F4A6562616E794377656C4B757277794E6965436863655A6E61634C4D414F'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=2)
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(tasks, url_prefix='/tasks')


@app.route('/')
def hello_world():
    return redirect(url_for('users.login'))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
