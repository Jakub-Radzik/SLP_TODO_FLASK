# client = MongoClient('mongodb+srv://admin:admin@cluster0.ab4vr.mongodb.net/slp_todo?retryWrites=true&w=majority')
# db = client["slp_todo"]

# users_collection = db['users']
# tasks_collection = db['tasks']
# import pymongo
#
# print("Connecting to MongoDB")
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["slp_todo"]
# users_collection = mydb["users"]
# tasks_collection = mydb["tasks"]
#
# users_collection.insert_one({
#     "name": "admin",
#     "surname": "admin",
#     "username": "admin",
#     "email": "admin@admin.pl",
#     "password": "admin",
# })
#
# tasks_collection.insert_one({
#     "title": "Task 1",
#     "description": "Description 1",
# })
#
# print("inited")
import pymongo


class Database(object):
    db = None

    @staticmethod
    def init():
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        Database.db = client["slp_todo"]

    @staticmethod
    def insert(collection, data):
        Database.db[collection].insert_one(data)

    @staticmethod
    def find(collection, query):
        return Database.db[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.db[collection].find_one(query)

    @staticmethod
    def insert_one(collection, data):
        Database.db[collection].insert_one(data)

    @staticmethod
    def delete_one(collection, data):
        Database.db[collection].delete_one(data)

    @staticmethod
    def update_one(collection, data):
        Database.db[collection].update_one(data)

