from uuid import uuid4

from .connection import MongoConnection
from .models import CartItem, Category, Order, Product, Subcategory, UserProfile


class UserRepository:
    def __init__(self, connection: MongoConnection):
        self.collection = connection.collection("users")

    def get_by_user_id(self, user_id: int):
        document = self.collection.find_one({"user_id": user_id})
        if not document:
            return None
        return UserProfile.from_document(document)

    def set_field(self, user_id: int, field: str, value):
        self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"user_id": user_id, field: value}},
            upsert=True,
        )

    def set_name(self, user_id: int, name: str):
        self.set_field(user_id, "name", name)

    def set_number(self, user_id: int, number: str):
        self.set_field(user_id, "number", number)

    def set_age(self, user_id: int, age: int):
        self.set_field(user_id, "age", age)


class CatalogRepository:
    def __init__(self, connection: MongoConnection):
        self.catalog_collection = connection.collection("catalog")
        self.subcategories_collection = connection.collection("categories")
        self.products_collection = connection.collection("product")

    def list_categories(self):
        return [
            Category.from_document(item)
            for item in self.catalog_collection.find().sort("title")
        ]

    def get_category(self, title: str):
        document = self.catalog_collection.find_one({"title": title})
        if not document:
            return None
        return Category.from_document(document)

    def list_subcategories(self, category_title: str):
        return [
            Subcategory.from_document(item)
            for item in self.subcategories_collection.find(
                {"categories": category_title}
            ).sort("title")
        ]

    def get_subcategory(self, title: str):
        document = self.subcategories_collection.find_one({"title": title})
        if not document:
            return None
        return Subcategory.from_document(document)

    def list_products(self, subcategory_title: str):
        return [
            Product.from_document(item)
            for item in self.products_collection.find(
                {"categories": subcategory_title}
            ).sort("title")
        ]

    def get_product(self, title: str):
        document = self.products_collection.find_one({"title": title})
        if not document:
            return None
        return Product.from_document(document)


class CartRepository:
    def __init__(self, connection: MongoConnection):
        self.collection = connection.collection("history")

    def add_item(self, user_id: int, product: Product):
        self.collection.insert_one(
            {
                "user_id": user_id,
                "product": product.title,
                "description": product.description,
                "price": product.price,
            }
        )

    def list_items(self, user_id: int):
        return [
            CartItem.from_document(item)
            for item in self.collection.find({"user_id": user_id})
        ]

    def remove_item(self, user_id: int, product_title: str):
        self.collection.delete_one({"user_id": user_id, "product": product_title})

    def clear(self, user_id: int):
        self.collection.delete_many({"user_id": user_id})


class OrderRepository:
    def __init__(self, connection: MongoConnection):
        self.collection = connection.collection("cart")

    def create_order(self, user_id: int, user: UserProfile, item: CartItem):
        self.collection.insert_one(
            {
                "user_id": user_id,
                "name": user.name,
                "number": user.number,
                "age": user.age,
                "product": item.product,
                "price": item.price,
                "track": f"YUHU-{uuid4().hex[:10].upper()}",
                "status": "Ожидает",
            }
        )

    def list_orders(self, user_id: int):
        return [
            Order.from_document(item)
            for item in self.collection.find({"user_id": user_id})
        ]
