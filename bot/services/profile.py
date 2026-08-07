from bot.database.repositories import UserRepository


class ProfileService:
    def __init__(self, users: UserRepository):
        self.users = users

    def get_profile(self, user_id: int):
        return self.users.get_by_user_id(user_id)

    def save_name(self, user_id: int, name: str):
        self.users.set_name(user_id, name)

    def save_number(self, user_id: int, number: str):
        self.users.set_number(user_id, number)

    def save_age(self, user_id: int, age: int):
        self.users.set_age(user_id, age)
