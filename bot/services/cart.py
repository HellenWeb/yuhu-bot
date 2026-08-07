from bot.database.repositories import CartRepository
from bot.services.catalog import CatalogService


class CartService:
    def __init__(self, cart: CartRepository, catalog: CatalogService):
        self.cart = cart
        self.catalog = catalog

    def list_items(self, user_id: int):
        return self.cart.list_items(user_id)

    def add_product(self, user_id: int, product_title: str):
        product = self.catalog.get_product(product_title)
        if not product:
            return None
        self.cart.add_item(user_id, product)
        return product

    def remove_product(self, user_id: int, product_title: str):
        self.cart.remove_item(user_id, product_title)

    def clear(self, user_id: int):
        self.cart.clear(user_id)
