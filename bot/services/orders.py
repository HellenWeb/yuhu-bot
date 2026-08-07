from bot.database.repositories import CartRepository, OrderRepository, UserRepository


class OrderService:
    def __init__(
        self,
        users: UserRepository,
        cart: CartRepository,
        orders: OrderRepository,
    ):
        self.users = users
        self.cart = cart
        self.orders = orders

    def list_orders(self, user_id: int):
        return self.orders.list_orders(user_id)

    def checkout(self, user_id: int) -> str:
        profile = self.users.get_by_user_id(user_id)
        if not profile or not profile.is_complete:
            return "profile_required"

        if not profile.is_adult:
            return "underage"

        items = self.cart.list_items(user_id)
        if not items:
            return "cart_empty"

        for item in items:
            self.orders.create_order(user_id, profile, item)

        self.cart.clear(user_id)
        return "success"
