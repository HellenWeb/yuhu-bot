
# Modules

import sqlite3

# Logic

class SQLighter:
    def __init__(self, db_name):
        self.connect = sqlite3.connect(db_name)
        self.cursor = self.connect.cursor()
    def inster_name(self, user_id, name):
        with self.connect:
            self.cursor.execute(f'INSERT INTO `users` (`user_id`, `name`) VALUES ("{user_id}", "{name}")')
    def inster_number(self, user_id, number):
        with self.connect:
            self.cursor.execute(f'INSERT INTO `users` (`user_id`, `number`) VALUES ("{user_id}", "{number}")')
    def inster_age(self, user_id, age):
        with self.connect:
            self.cursor.execute(f'INSERT INTO `users` (`user_id`, `age`) VALUES ("{user_id}", "{age}")')
    def update_name(self, user_id, name):
        with self.connect:
            self.cursor.execute(f'UPDATE `users` SET `name` = "{name}" WHERE `user_id` = {user_id}')
    def update_number(self, user_id, number):
        with self.connect:
            self.cursor.execute(f'UPDATE `users` SET `number` = {number} WHERE `user_id` = {user_id}')
    def update_age(self, user_id, age):
        with self.connect:
            self.cursor.execute(f'UPDATE `users` SET `age` = {age} WHERE `user_id` = {user_id}')
    def show_name(self, user_id):
        with self.connect:
            return self.cursor.execute(f'SELECT name FROM `users` WHERE `user_id` = ?', (user_id,)).fetchone()
    def show_number(self, user_id):
        with self.connect:
            return self.cursor.execute(f'SELECT number FROM `users` WHERE `user_id` = ?', (user_id,)).fetchone()
    def show_age(self, user_id):
        with self.connect:
            return self.cursor.execute(f'SELECT age FROM `users` WHERE `user_id` = ?', (user_id,)).fetchone()
    def show_under_categories(self, categories):
        with self.connect:
            return self.cursor.execute(f'SELECT `title` FROM `categories` WHERE `categories` = ?', (categories,)).fetchall()
    def show_categories(self):
        with self.connect:
            return self.cursor.execute(f'SELECT categorie FROM `catalog`').fetchall()
    def show_product(self, categories):
        with self.connect:
            return self.cursor.execute(f'SELECT * FROM `product` WHERE `categories` = ?', (categories,)).fetchall()
    def close(self):
        self.connect.close()