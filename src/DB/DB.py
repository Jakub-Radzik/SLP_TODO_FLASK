# client = MongoClient('mongodb+srv://admin:admin@cluster0.ab4vr.mongodb.net/slp_todo?retryWrites=true&w=majority')
# db = client["slp_todo"]

# users_collection = db['users']
# tasks_collection = db['tasks']
import pymongo

print("Connecting to MongoDB")
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["slp_todo"]
users_collection = mydb["users"]
tasks_collection = mydb["tasks"]

users_collection.insert_one({
    "name": "admin",
    "surname": "admin",
    "username": "admin",
    "email": "admin@admin.pl",
    "password": "admin",
})

tasks_collection.insert_one({
    "title": "Task 1",
    "description": "Description 1",
})

print("inited")