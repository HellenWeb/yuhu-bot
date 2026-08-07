from aiogram import types


HOME_CALLBACK = "home"
BACK_CALLBACK = "back"
CATEGORY_PREFIX = "cat"
SUBCATEGORY_PREFIX = "sub"
ADD_TO_CART_PREFIX = "add"
DELETE_FROM_CART_PREFIX = "delete"


def _encode(prefix: str, value: str) -> str:
    return f"{prefix}:{value}"


def decode_value(data: str) -> str:
    return data.split(":", 1)[1]


def build_catalog_keyboard(categories):
    markup = types.InlineKeyboardMarkup(row_width=True)
    for category in categories:
        markup.row(
            types.InlineKeyboardButton(
                text=category.title,
                callback_data=_encode(CATEGORY_PREFIX, category.title),
            )
        )
    markup.add(types.InlineKeyboardButton(text="🏠", callback_data=HOME_CALLBACK))
    return markup


def build_subcategories_keyboard(subcategories):
    markup = types.InlineKeyboardMarkup(row_width=True)
    for subcategory in subcategories:
        markup.row(
            types.InlineKeyboardButton(
                text=subcategory.title,
                callback_data=_encode(SUBCATEGORY_PREFIX, subcategory.title),
            )
        )
    markup.add(types.InlineKeyboardButton(text="⬅️", callback_data=BACK_CALLBACK))
    return markup


def build_product_keyboard(product):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(
            text="Добавить в корзину 🛍",
            callback_data=_encode(ADD_TO_CART_PREFIX, product.title),
        )
    )
    return markup


def build_delete_keyboard(product_title: str):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(
            text="❌",
            callback_data=_encode(DELETE_FROM_CART_PREFIX, product_title),
        )
    )
    return markup
