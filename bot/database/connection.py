from pymongo import ASCENDING, MongoClient


class MongoConnection:
    def __init__(self, uri: str, db_name: str):
        self._client = MongoClient(uri)
        self.db = self._client[db_name]
        self._ensure_indexes()

    def collection(self, name: str):
        return self.db[name]

    def close(self):
        self._client.close()

    def _ensure_indexes(self):
        self.collection("users").create_index([("user_id", ASCENDING)], unique=True)
        self.collection("history").create_index([("user_id", ASCENDING)])
        self.collection("cart").create_index([("user_id", ASCENDING)])
        self.collection("catalog").create_index([("title", ASCENDING)])
        self.collection("categories").create_index([("categories", ASCENDING)])
        self.collection("product").create_index([("categories", ASCENDING)])
        self.collection("product").create_index([("title", ASCENDING)])
