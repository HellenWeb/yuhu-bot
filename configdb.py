
from dispacher import mongo

for i in mongo.show_cart(838087888):
    print(i)

# from pymongo import MongoClient
#
# class MongoDB:
#     def __init__(self, db_name):
#         self.connect = MongoClient(db_name)
#         self.cursor = self.connect["test_db"]
#     def insert(self, user_id, name):
#         with self.connect:
#             self.cursor["test_collection"].insert_one({"user_id": user_id, "name": name})
#     def show_user(self, name):
#         with self.connect:
#             return self.cursor['test_collection'].find({"name": name})
#     def close(self):
#         with self.connect:
#             self.connect.close()

# mongo.insert("8260989", "Alex")

# mongo = MongoClient("mongodb+srv://Hellen:fbnz32iZA1ho49iy@cluster0.aqrqr.mongodb.net/yuhu-bot?retryWrites=true&w=majority")
# base = mongo["test_db"]
# def show(name):
#     return base['test_collection'].find({"name": name})
# for i in show("Alex"):
#     print(i)
