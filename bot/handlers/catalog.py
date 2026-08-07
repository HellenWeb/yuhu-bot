from bot.keyboards.inline import (
    ADD_TO_CART_PREFIX,
    BACK_CALLBACK,
    CATEGORY_PREFIX,
    HOME_CALLBACK,
    SUBCATEGORY_PREFIX,
    decode_value,
)
from bot.texts import ADD_TO_CART_SUCCESS_TEXT


def register(dispatcher, services):
    catalog = services.catalog
    cart = services.cart
    views = services.views

    @dispatcher.message_handler(commands=["catalog"])
    async def catalog_command(message):
        await views.send_catalog(message)

    @dispatcher.message_handler(
        lambda message: message.text in {"Каталог 🛒", "🛒"},
        state=None,
    )
    async def catalog_button(message):
        await views.send_catalog(message)

    @dispatcher.callback_query_handler(lambda callback: callback.data == HOME_CALLBACK)
    async def home_callback(callback):
        await views.send_main_menu(callback.message)
        await callback.answer()

    @dispatcher.callback_query_handler(lambda callback: callback.data == BACK_CALLBACK)
    async def back_callback(callback):
        await views.edit_catalog(callback)
        await callback.answer()

    @dispatcher.callback_query_handler(
        lambda callback: callback.data
        and callback.data.startswith(f"{CATEGORY_PREFIX}:")
    )
    async def category_callback(callback):
        category_title = decode_value(callback.data)
        if not catalog.get_category(category_title):
            await callback.answer("Категория не найдена", show_alert=True)
            return
        await views.send_subcategories(callback, category_title)
        await callback.answer()

    @dispatcher.callback_query_handler(
        lambda callback: callback.data
        and callback.data.startswith(f"{SUBCATEGORY_PREFIX}:")
    )
    async def subcategory_callback(callback):
        subcategory_title = decode_value(callback.data)
        if not catalog.get_subcategory(subcategory_title):
            await callback.answer("Подкатегория не найдена", show_alert=True)
            return
        await views.send_products(callback, subcategory_title)
        await callback.answer()

    @dispatcher.callback_query_handler(
        lambda callback: callback.data
        and callback.data.startswith(f"{ADD_TO_CART_PREFIX}:")
    )
    async def add_to_cart_callback(callback):
        product_title = decode_value(callback.data)
        product = cart.add_product(callback.from_user.id, product_title)
        if not product:
            await callback.answer("Товар не найден", show_alert=True)
            return

        await callback.message.answer(
            ADD_TO_CART_SUCCESS_TEXT.format(title=product.title),
            parse_mode="html",
        )
        await callback.answer()
