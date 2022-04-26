from pymongo import MongoClient

client = MongoClient('mongodb+srv://admin:admin@cluster0.ab4vr.mongodb.net/slp_todo?retryWrites=true&w=majority')
db = client["slp_todo"]
users_collection = db['users']
tasks_collection = db['tasks']