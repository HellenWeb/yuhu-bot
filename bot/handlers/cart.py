from aiogram.dispatcher.filters import Text

from bot.keyboards.inline import DELETE_FROM_CART_PREFIX, decode_value
from bot.texts import (
    BUY_REQUIRES_PROFILE_TEXT,
    BUY_SUCCESS_TEXT,
    CART_EMPTY_TEXT,
    DELETE_FROM_CART_SUCCESS_TEXT,
    MINOR_SELLING_BLOCK_TEXT,
)


def register(dispatcher, services):
    cart = services.cart
    orders = services.orders
    views = services.views

    @dispatcher.message_handler(commands=["cart"])
    async def cart_command(message):
        await views.send_cart(message)

    @dispatcher.message_handler(
        Text(equals=["Корзина 🛍", "🛍", "Обновить"]),
        state=None,
    )
    async def cart_button(message):
        await views.send_cart(message)

    @dispatcher.message_handler(Text(equals="Купить всё"), state=None)
    async def checkout_button(message):
        result = orders.checkout(message.from_user.id)
        messages = {
            "profile_required": BUY_REQUIRES_PROFILE_TEXT,
            "underage": MINOR_SELLING_BLOCK_TEXT,
            "cart_empty": CART_EMPTY_TEXT,
            "success": BUY_SUCCESS_TEXT,
        }
        await message.answer(
            messages[result],
            parse_mode="html",
        )

    @dispatcher.callback_query_handler(
        lambda callback: callback.data
        and callback.data.startswith(f"{DELETE_FROM_CART_PREFIX}:")
    )
    async def delete_from_cart_callback(callback):
        product_title = decode_value(callback.data)
        cart.remove_product(callback.from_user.id, product_title)
        await callback.message.answer(
            DELETE_FROM_CART_SUCCESS_TEXT.format(title=product_title),
            parse_mode="html",
        )
        await callback.answer()
