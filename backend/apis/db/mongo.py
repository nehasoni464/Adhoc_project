from flask import g
from pymongo import MongoClient
import os


class Database():
    def __init__(self):
        if 'db' not in g:
            g.db = MongoClient('mongodb+srv://kunal:adhoc123@cluster0-0e7nv.mongodb.net')
        self.db = g.db.get_database('adhoc')
        self.user_col = self.db.get_collection('users')
        self.dockerhost = self.db.get_collection('dockerhost')

    def close_db(self):
        db = g.pop('db', None)
        if db is not None:
            db.close()


# from pymongo import MongoClient
# from flask import g
# import os


# class Mongo():

#     def _init_(self):
#         if 'db' not in g:
#             client = MongoClient(os.getenv('db'))
#             g.db = client.get_database('_IMS_')
#         self.db = g.db
#         self.indents = self.db.get_collection('indents')
#         self.users = self.db.get_collection('users')
#         self.transporters = self.db.get_collection('transporters')
#         self.locations = self.db.get_collection('locations')
#         self.freight = self.db.get_collection('freight')

#     def create_user(self, data):
#         resp = self.users.insert_one(data)
#         return resp

#     def get_user(self, username):
#         return self.users.find_one({"username": username})