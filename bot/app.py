import logging
from dataclasses import dataclass

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.config import settings
from bot.database.connection import MongoConnection
from bot.database.repositories import (
    CartRepository,
    CatalogRepository,
    OrderRepository,
    UserRepository,
)
from bot.services import Services
from bot.services.cart import CartService
from bot.services.catalog import CatalogService
from bot.services.orders import OrderService
from bot.services.profile import ProfileService
from bot.services.views import ViewService


@dataclass(frozen=True)
class AppContext:
    bot: Bot
    dispatcher: Dispatcher
    connection: MongoConnection
    services: Services


def create_app() -> AppContext:
    logging.basicConfig(level=logging.INFO)

    connection = MongoConnection(settings.mongo_uri, settings.mongo_db_name)
    bot = Bot(settings.bot_token, parse_mode="html")
    dispatcher = Dispatcher(bot, storage=MemoryStorage())

    user_repository = UserRepository(connection)
    catalog_repository = CatalogRepository(connection)
    cart_repository = CartRepository(connection)
    order_repository = OrderRepository(connection)

    profile_service = ProfileService(user_repository)
    catalog_service = CatalogService(catalog_repository, settings)
    cart_service = CartService(cart_repository, catalog_service)
    order_service = OrderService(user_repository, cart_repository, order_repository)
    view_service = ViewService(
        bot=bot,
        profile_service=profile_service,
        catalog_service=catalog_service,
        cart_service=cart_service,
        order_service=order_service,
    )

    services = Services(
        profile=profile_service,
        catalog=catalog_service,
        cart=cart_service,
        orders=order_service,
        views=view_service,
    )

    return AppContext(
        bot=bot,
        dispatcher=dispatcher,
        connection=connection,
        services=services,
    )
