# Modules

from random import randint as r
from pymongo import MongoClient

# Logic

# ---------- DELETED --------------

# class SQLighter:
#     def __init__(self, db_name):
#         self.connect = sqlite3.connect(db_name)
#         self.cursor = self.connect.cursor()
#     def inster_name(self, user_id, name):
#         with self.connect:
#             self.cursor.execute(f'INSERT INTO `users` (`user_id`, `name`) VALUES ("{user_id}", "{name}")')
#     def inster_number(self, user_id, number):
#         with self.connect:
#             self.cursor.execute(f'INSERT INTO `users` (`user_id`, `number`) VALUES ("{user_id}", "{number}")')
#     def inster_age(self, user_id, age):
#         with self.connect:
#             self.cursor.execute(f'INSERT INTO `users` (`user_id`, `age`) VALUES ("{user_id}", "{age}")')
#     def update_name(self, user_id, name):
#         with self.connect:
#             self.cursor.execute(f'UPDATE `users` SET `name` = "{name}" WHERE `user_id` = {user_id}')
#     def update_number(self, user_id, number):
#         with self.connect:
#             self.cursor.execute(f'UPDATE `users` SET `number` = {number} WHERE `user_id` = {user_id}')
#     def update_age(self, user_id, age):
#         with self.connect:
#             self.cursor.execute(f'UPDATE `users` SET `age` = {age} WHERE `user_id` = {user_id}')
#     def show_name(self, user_id):
#         with self.connect:
#             return self.cursor.execute(f'SELECT name FROM `users` WHERE `user_id` = ?', (user_id,)).fetchone()
#     def show_number(self, user_id):
#         with self.connect:
#             return self.cursor.execute(f'SELECT number FROM `users` WHERE `user_id` = ?', (user_id,)).fetchone()
#     def show_age(self, user_id):
#         with self.connect:
#             return self.cursor.execute(f'SELECT age FROM `users` WHERE `user_id` = ?', (user_id,)).fetchone()
#     def show_under_categories(self, categories):
#         with self.connect:
#             return self.cursor.execute(f'SELECT `title` FROM `categories` WHERE `categories` = ?', (categories,)).fetchall()
#     def show_categories(self):
#         with self.connect:
#             return self.cursor.execute(f'SELECT categorie FROM `catalog`').fetchall()
#     def delete_all_history(self, user_id):
#         with self.connect:
#             self.cursor.execute(f'DELETE FROM `history` WHERE `user_id` = "{user_id}"')
#     def delete_history(self, user_id, product):
#         with self.connect:
#             self.cursor.execute(f'DELETE FROM `history` WHERE `user_id` = "{user_id}" AND `product` = "{product}"')
#     def show_product(self, categories):
#         with self.connect:
#             return self.cursor.execute(f'SELECT * FROM `product` WHERE `categories` = ?', (categories,)).fetchall()
#     def inster_cart(self, user_id, name, number, age, product):
#         with self.connect:
#             self.cursor.execute(f'INSERT INTO `cart` (`user_id`, `name`, `number`, `age`, `product`, `track`) VALUES ("{user_id}", "{name}", {number}, {age}, "{product}", "{r(1, 10000000000)}")')
#     def show_cart(self, user_id):
#         with self.connect:
#             return self.cursor.execute(f'SELECT * FROM `cart` WHERE `user_id` = ?', (user_id,)).fetchall()
#     def inster_history(self, user_id, product, description, price):
#         with self.connect:
#             self.cursor.execute(f'INSERT INTO `history` (`user_id`, `product`, `description`, `price`) VALUES ("{user_id}", "{product}", "{description}", "{price}")')
#     def show_history(self, user_id):
#         with self.connect:
#             return self.cursor.execute(f'SELECT * FROM `history` WHERE `user_id` = ?', (user_id,)).fetchall()
#     def close(self):
#         self.connect.close()

"""Class for Database"""


class MongoDB:
    def __init__(self, db_name):
        self.connect = MongoClient(db_name)
        self.cursor = self.connect["test_db"]

    def inster_name(self, user_id, name):
        self.cursor["users"].insert_one({"user_id": user_id, "name": name})

    def inster_number(self, user_id, number):
        self.cursor["users"].insert_one({"user_id": user_id, "number": number})

    def inster_age(self, user_id, age):
        self.cursor["users"].insert_one({"user_id": user_id, "age": age})

    def update_name(self, user_id, name):
        self.cursor["users"].update_one({"user_id": user_id}, {"$set": {"name": name}})

    def update_number(self, user_id, number):
        self.cursor["users"].update_one(
            {"user_id": user_id}, {"$set": {"number": number}}
        )

    def update_age(self, user_id, age):
        self.cursor["users"].update_one({"user_id": user_id}, {"$set": {"age": age}})

    def show_users(self, user_id):
        return self.cursor["users"].find_one({"user_id": user_id})

    def show_under_categories(self, categories):
        return self.cursor["categories"].find({"categories": categories})

    def show_categories(self):
        return self.cursor["catalog"].find()

    def delete_all_history(self, user_id):
        self.cursor["history"].delete_many({"user_id": user_id})

    def delete_history(self, user_id, product):
        self.cursor["history"].delete_one({"user_id": user_id, "product": product})

    def inster_cart(self, user_id, name, number, age, product, price):
        self.cursor["cart"].insert_one(
            {
                "user_id": user_id,
                "name": name,
                "number": number,
                "age": age,
                "product": product,
                "price": price,
                "track": r(1, 10000000000),
                "status": "Ожидает",
            }
        )

    def show_cart(self, user_id):
        return self.cursor["cart"].find({"user_id": user_id})

    def show_product(self, categories):
        return self.cursor["product"].find({"categories": categories})

    def inster_history(self, user_id, product, description, price):
        self.cursor["history"].insert_one(
            {
                "user_id": user_id,
                "product": product,
                "description": description,
                "price": price,
            }
        )

    def show_history(self, user_id):
        return self.cursor["history"].find({"user_id": user_id})

    def close(self):
        self.connect.close()
