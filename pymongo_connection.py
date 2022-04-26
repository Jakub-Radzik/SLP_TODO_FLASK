from pymongo import MongoClient
from os import environ


def get_database():
    client = MongoClient("mongodb+srv://admin:admin@Cluster0.ab4vr.mongodb.net")
    return client['slp_todo']