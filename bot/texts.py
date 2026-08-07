from bot.database.models import CartItem, Order, Product, UserProfile


MAIN_MENU_TEXT = (
    "Привет {name} 😁\n"
    "<strong>Это телеграмм бот магазина ЮХУ</strong>\n"
    "Здесь ты сможешь купить нужный тебе товар и забрать его в ближайшем нашем магазине\n"
    "Creator: @YungHellen"
)

ABOUT_TEXT = (
    "Магазин тобачной продукции ЮХУ\nНаши магазины находятся в Владивостоке, "
    "Хабаровске, Сахалине, Улан-Удэ и Магадане\n\n<strong>Владивосток</strong>: "
    "ул. Луговая, 18; ул. Семёновская, 23\n<strong>Южно-Сахалинск</strong>: "
    "ул. Комсомольская, 157; ул.Пуркаева, 65\n<strong>Хабаровск</strong>: "
    "Амурский Бульвар 56\n<strong>Корсаков</strong>: ул.Корсаковская, 10\n"
    "<strong>Улан-Удэ</strong>: ул.Ербанова, 20; ул.Терешкова, 14\n"
    "<strong>Магадан</strong>: Проспект Карла Маркса, 23"
)

HELP_TEXT = (
    "/start или /help - <strong>Главное меню</strong>\n"
    "/settings - <strong>Настройки</strong>\n"
    "/catalog - <strong>Каталог</strong>\n"
    "/about - <strong>О нас</strong>\n"
    "/cart - <strong>Корзина</strong>\n"
    "/history - <strong>История покупок</strong>\n\n"
    "Выберите ниже раздел справки и получите краткую помощь. Если Ваш вопрос "
    "не решен, обратитесь за помощью к живому оператору @YungHellen."
)

SETTINGS_EMPTY_TEXT = (
    "ID - {user_id}\n"
    "Имя в telegram - {telegram_name}\n"
    "Имя - не введено\n"
    "Номер - не введено\n"
    "Возраст - не введено\n\n"
    "Чтобы поля стали видны нужно заполнить их всех"
)

CART_EMPTY_TEXT = "Корзина пуста 🚫\nПосмотрите наш /catalog"
ORDERS_EMPTY_TEXT = "Вы ничего у нас не заказывали 😁\nПосмотрите наш /catalog"
CATALOG_TEXT = "Категории товаров:"
SUBCATEGORIES_TEXT = "Подгруппы товаров:"
ADD_TO_CART_SUCCESS_TEXT = 'Товар <strong>{title}</strong> успешно добавлен в корзину'
DELETE_FROM_CART_SUCCESS_TEXT = "Товар успешно удален (<strong>{title}</strong>) ❎"
BUY_REQUIRES_PROFILE_TEXT = "Заполните все поля в /settings"
MINOR_SELLING_BLOCK_TEXT = "Лицам младше 18 лет продажа тобачной продукции запрещена ⛔️"
BUY_SUCCESS_TEXT = (
    "<strong>Все товары успешно куплены</strong> ✅\n"
    "Вы сможете забрать все товары в наших магазинах /about, просто показав "
    "track-номер\n<strong>Спасибо за покупку</strong> 😃"
)
INVALID_AGE_TEXT = "Возраст должен быть указан числом"
INVALID_AGE_RANGE_TEXT = "Введите корректный возраст"
PRODUCTS_SUMMARY_TEXT = "Показаны все товары ({count})"
PRODUCT_WITHOUT_PHOTO_TEXT = "У товара нет фотографии ❌"

PROFILE_FIELD_PROMPTS = {
    "name": "Введи свое имя",
    "number": "Введи свой номер",
    "age": "Введите свой возраст",
}

PROFILE_FIELD_SAVE_TEXTS = {
    "name": "Имя сохранено",
    "number": "Номер сохранен",
    "age": "Возраст сохранен",
}


def format_main_menu_text(name: str) -> str:
    return MAIN_MENU_TEXT.format(name=name)


def format_settings_text(user_id: int, telegram_name: str, profile: UserProfile | None) -> str:
    if not profile or not profile.is_complete:
        return SETTINGS_EMPTY_TEXT.format(
            user_id=user_id,
            telegram_name=telegram_name,
        )

    age_suffix = " <strong>(меньше 18!)</strong>" if not profile.is_adult else ""
    return (
        f"ID - {user_id}\n"
        f"Имя в telegram - {telegram_name}\n"
        f"Имя - {profile.name}\n"
        f"Номер - +{profile.number}\n"
        f"Возраст - {profile.age}{age_suffix}"
    )


def format_cart_item_text(item: CartItem) -> str:
    return (
        f"<strong>Название: </strong>{item.product}\n"
        f"<strong>Описание: </strong>{item.description}\n"
        f"<strong>Цена:</strong> {item.price}"
    )


def format_cart_summary(count: int, total: int) -> str:
    return f"Корзина ({count}) & Общая сумма <strong>{total} руб.</strong>"


def format_order_text(order: Order) -> str:
    return (
        f"Товар - <strong>{order.product}</strong>\n"
        f"Статус доставки - <strong>{order.status}</strong>\n"
        f"Track - <strong>{order.track}</strong>\n\n"
    )


def format_product_text(product: Product, has_photo: bool) -> str:
    text = (
        f"<strong>Название: </strong>{product.title}\n"
        f"<strong>Описание: </strong>{product.description}\n"
        f"<strong>Цена:</strong> {product.price} руб."
    )
    if has_photo:
        return text
    return f"{text}\n\n{PRODUCT_WITHOUT_PHOTO_TEXT}"
