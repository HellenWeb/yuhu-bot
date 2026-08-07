from aiogram import types


def build_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Настройки 📎", "Помощь ❓")
    markup.row("Заказы 📦", "Каталог 🛒")
    markup.row("Корзина 🛍", "О нас ❕")
    return markup


def build_settings_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Имя", "Номер", "Возраст")
    markup.row("⬅️")
    markup.add(types.KeyboardButton(text="🏠"))
    return markup


def build_cart_actions_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Купить всё", "Обновить")
    markup.row("🏠")
    return markup


def build_products_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🏠", "🛒", "🛍")
    return markup
