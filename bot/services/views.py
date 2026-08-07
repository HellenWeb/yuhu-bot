from aiogram import Bot

from bot.keyboards.inline import (
    build_catalog_keyboard,
    build_delete_keyboard,
    build_product_keyboard,
    build_subcategories_keyboard,
)
from bot.keyboards.reply import (
    build_cart_actions_menu,
    build_main_menu,
    build_products_menu,
    build_settings_menu,
)
from bot.texts import (
    ABOUT_TEXT,
    CATALOG_TEXT,
    CART_EMPTY_TEXT,
    HELP_TEXT,
    ORDERS_EMPTY_TEXT,
    PRODUCTS_SUMMARY_TEXT,
    SUBCATEGORIES_TEXT,
    format_cart_item_text,
    format_cart_summary,
    format_main_menu_text,
    format_order_text,
    format_product_text,
    format_settings_text,
)


class ViewService:
    def __init__(self, bot: Bot, profile_service, catalog_service, cart_service, order_service):
        self.bot = bot
        self.profile_service = profile_service
        self.catalog_service = catalog_service
        self.cart_service = cart_service
        self.order_service = order_service

    async def send_main_menu(self, message):
        await message.answer(
            format_main_menu_text(message.from_user.first_name),
            parse_mode="html",
            reply_markup=build_main_menu(),
        )

    async def send_help(self, message):
        await message.answer(HELP_TEXT, parse_mode="html")

    async def send_about(self, message):
        await message.answer(ABOUT_TEXT, parse_mode="html")

    async def send_settings(self, message):
        profile = self.profile_service.get_profile(message.from_user.id)
        await message.answer(
            format_settings_text(
                user_id=message.from_user.id,
                telegram_name=message.from_user.first_name,
                profile=profile,
            ),
            parse_mode="html",
            reply_markup=build_settings_menu(),
        )

    async def send_catalog(self, message):
        categories = self.catalog_service.list_categories()
        await message.answer(
            CATALOG_TEXT,
            reply_markup=build_catalog_keyboard(categories),
        )

    async def edit_catalog(self, callback):
        categories = self.catalog_service.list_categories()
        await self.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=CATALOG_TEXT,
            reply_markup=build_catalog_keyboard(categories),
        )

    async def send_subcategories(self, callback, category_title: str):
        subcategories = self.catalog_service.list_subcategories(category_title)
        await self.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=SUBCATEGORIES_TEXT,
            reply_markup=build_subcategories_keyboard(subcategories),
        )

    async def send_products(self, callback, subcategory_title: str):
        products = self.catalog_service.list_products(subcategory_title)
        count = 0

        for product in products:
            picture_path = self.catalog_service.get_product_picture_path(product)
            has_photo = bool(picture_path and picture_path.exists())
            if has_photo:
                with open(picture_path, "rb") as picture:
                    await callback.message.answer_photo(picture)

            await callback.message.answer(
                format_product_text(product, has_photo=has_photo),
                parse_mode="html",
                reply_markup=build_product_keyboard(product),
            )
            count += 1

        await callback.message.answer(
            PRODUCTS_SUMMARY_TEXT.format(count=count),
            reply_markup=build_products_menu(),
        )

    async def send_cart(self, message):
        items = self.cart_service.list_items(message.from_user.id)
        if not items:
            await message.answer(CART_EMPTY_TEXT)
            return

        total = 0
        for item in items:
            await message.answer(
                format_cart_item_text(item),
                parse_mode="html",
                reply_markup=build_delete_keyboard(item.product),
            )
            total += item.price

        await message.answer(
            format_cart_summary(len(items), total),
            parse_mode="html",
            reply_markup=build_cart_actions_menu(),
        )

    async def send_orders(self, message):
        orders = self.order_service.list_orders(message.from_user.id)
        if not orders:
            await message.answer(ORDERS_EMPTY_TEXT)
            return

        for order in orders:
            await message.answer(format_order_text(order), parse_mode="html")
