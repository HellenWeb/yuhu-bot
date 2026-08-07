from dataclasses import dataclass

from .cart import CartService
from .catalog import CatalogService
from .orders import OrderService
from .profile import ProfileService
from .views import ViewService


@dataclass(frozen=True)
class Services:
    profile: ProfileService
    catalog: CatalogService
    cart: CartService
    orders: OrderService
    views: ViewService
