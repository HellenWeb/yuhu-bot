from .about import register as register_about
from .catalog import register as register_catalog
from .common import register as register_common
from .cart import register as register_cart
from .orders import register as register_orders
from .profile import register as register_profile


def register_handlers(dispatcher, services):
    register_common(dispatcher, services)
    register_about(dispatcher, services)
    register_profile(dispatcher, services)
    register_catalog(dispatcher, services)
    register_cart(dispatcher, services)
    register_orders(dispatcher, services)
