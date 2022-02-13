
# Modules

from dispacher import db, bot, mongo
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, executor

# Class State

"""Class for states"""

class FSMSettings(StatesGroup):
    name = State()
    number = State()
    age = State()

# Logic

"""Start message display function"""

@db.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    mark1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark1.row("Настройки 📎", "Помощь ❓")
    mark1.row("Заказы 📦", "Каталог 🛒")
    mark1.row("Корзина 🛍", "О нас ❕")
    await message.answer(f"Привет {message.from_user.first_name} 😁\n<strong>Это телеграмм бот магазина ЮХУ</strong>\nЗдесь ты сможешь купить нужный тебе товар и забрать его в ближайшем нашем магазине\nCreator: @YungHellen", parse_mode="html", reply_markup=mark1)

"""Function to show all commands in the bot"""

@db.message_handler(commands=['history'])
async def history(message: types.Message):
    if mongo.show_cart(message.from_user.id):
        for i in mongo.show_cart(message.from_user.id):
            await message.answer(f'Товар - <strong>{i["product"]}</strong>\nСтатус доставки - <strong>{i["status"]}</strong>\nTrack - <strong>{i["track"]}</strong>\n\n', parse_mode='html')
    else:
        await message.answer(f'Вы ничего у нас не заказывали 😁\nПосмотрите наш /catalog')

"""Save the name to the database and cache"""

@db.message_handler(state=FSMSettings.name)
async def upload_name(message: types.message, state: FSMContext):
    """Detected data"""
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Имя сохранено')
    """Checking in the database"""
    if mongo.show_users(message.from_user.id):
        mongo.update_name(message.from_user.id, data['name'])
    else:
        mongo.inster_name(message.from_user.id, data['name'])
    await state.finish()

"""Save the number to the database and cache"""

@db.message_handler(state=FSMSettings.number)
async def upload_name(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = message.text
    await message.answer('Номер сохранен')
    if mongo.show_users(message.from_user.id):
        mongo.update_number(message.from_user.id, data['number'])
    else:
        mongo.inster_number(message.from_user.id, data['number'])
    await state.finish()

"""Save the age to the database and cache"""

@db.message_handler(state=FSMSettings.age)
async def upload_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer('Возраст сохранен')
    if mongo.show_users(message.from_user.id):
        mongo.update_age(message.from_user.id, data['age'])
    else:
        mongo.inster_age(message.from_user.id, data['age'])
    await state.finish()

"""Function to show all data about user"""

@db.message_handler(commands=['settings'])
async def settings(message: types.Message):
    mark1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text="🏠")
    mark1.row("Имя", "Номер", "Возраст")
    mark1.row('⬅️')
    mark1.add(btn1)
    """Checking data"""
    try:
        if int(mongo.show_users(message.from_user.id)["age"]) < 18:
            await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {mongo.show_users(message.from_user.id)['name']}\nНомер - +{mongo.show_users(message.from_user.id)['number']}\nВозраст - {mongo.show_users(message.from_user.id)['age']} <strong>(меньше 18!)</strong>", reply_markup=mark1)
        else:
            await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {mongo.show_users(message.from_user.id)['name']}\nНомер - +{mongo.show_users(message.from_user.id)['number']}\nВозраст - {mongo.show_users(message.from_user.id)['age']}", reply_markup=mark1)
    except TypeError and KeyError:
        await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - не введено\nНомер - не введено\nВозраст - не введено\n\nЧтобы поля стали видны нужно заполнить их всех", reply_markup=mark1)

"""Function to show all catalog"""

@db.message_handler(commands=['catalog'])
async def catalog(message: types.Message):
    mark1 = types.InlineKeyboardMarkup(row_width=True)
    for i in mongo.show_categories():
        mark1.row(types.InlineKeyboardButton(text=i["title"], callback_data=i["title"]))
    mark1.add(types.InlineKeyboardButton(text="🏠", callback_data="home"))
    await message.answer(f"Категории товаров:", reply_markup=mark1)

"""Function to show everything in the cart"""

@db.message_handler(commands=['cart'])
async def cart(message: types.Message):
    if mongo.show_history(message.from_user.id):
        result = 0
        count = 0
        for i in mongo.show_history(message.from_user.id):
            mark3 = types.InlineKeyboardMarkup(row_width=1)
            mark3.add(types.InlineKeyboardButton(text=f"❌", callback_data=f"delete {i['product']}"))
            await message.answer(f"<strong>Название: </strong>{i['product']}\n<strong>Описание: </strong>{i['description']}\n<strong>Цена:</strong> {i['price']}", reply_markup=mark3)
            result += int(i['price'])
            count += 1
        mark2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mark2.row(f"Купить всё", "Обновить")
        mark2.row(f"🏠")
        await message.answer(f"Корзина ({count}) & Общая сумма <strong>{result} руб.</strong>", reply_markup=mark2, parse_mode='html')
    else:
        await message.answer("Корзина пуста 🚫\nПосмотрите наш /catalog")

"""Function to show all data about company"""

@db.message_handler(commands=['about'])
async def about(message: types.Message):
    await message.answer("Магазин тобачной продукции ЮХУ\nНаши магазины находятся в Владивостоке, Хабаровске, Сахалине, Улан-Удэ и Магадане\n\n<strong>Владивосток</strong>: ул. Луговая, 18; ул. Семёновская, 23\n<strong>Южно-Сахалинск</strong>: ул. Комсомольская, 157; ул.Пуркаева, 65\n<strong>Хабаровск</strong>: Амурский Бульвар 56\n<strong>Корсаков</strong>: ул.Корсаковская, 10\n<strong>Улан-Удэ</strong>: ул.Ербанова, 20; ул.Терешкова, 14\n<strong>Магадан</strong>: Проспект Карла Маркса, 23")

"""Сallbacks of all inline buttons"""

@db.callback_query_handler(lambda c: True)
async def catalog(c: types.CallbackQuery):

    """Showing a subcatalog"""

    for i in mongo.show_categories():
        if c.data == i['title']:
            try:
                mark1 = types.InlineKeyboardMarkup(row_width=True)
                for n in mongo.show_under_categories(i["title"]):
                    mark1.row(types.InlineKeyboardButton(text=n["title"], callback_data=n["title"]))
                mark1.add(types.InlineKeyboardButton(text="⬅️", callback_data="back"))
                await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Подгруппы товаров:", reply_markup=mark1)

            except ZeroDivisionError:
                mark1 = types.InlineKeyboardMarkup(row_width=1)
                mark1.add(types.InlineKeyboardButton(text="⬅️", callback_data="back"))
                await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Подгруппы товаров:", reply_markup=mark1)
        for n in mongo.show_under_categories(i["title"]):
            if c.data == n["title"]:
                count = 0
                for f in mongo.show_product(n["title"]):
                    mark2 = types.InlineKeyboardMarkup(row_width=1)
                    mark2.add(types.InlineKeyboardButton(text=f"Добавить в корзину 🛍", callback_data=f["title"]))
                    mark2.add(types.InlineKeyboardButton(text=f'Купить - {f["price"]} руб.', callback_data=f["price"]))
                    await c.message.answer(f'<strong>Название: </strong>{f["title"]}\n<strong>Описание: </strong>{f["description"]}', reply_markup=mark2)
                    count += 1
                mark3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                mark3.row("🏠", "🛒", "🛍")
                await c.message.answer(f"Позаны все товары ({count})", reply_markup=mark3)
        for n in mongo.show_under_categories(i["title"]):
            for f in mongo.show_product(n["title"]):
                if c.data == f['title']:
                    try:
                        mongo.inster_history(c.from_user.id, f["title"], f["description"], f["price"])
                        await c.message.answer(f'Товар <strong>{f["title"]}</strong> успешно добавлен в корзину', parse_mode='html')
                    except TypeError and KeyError:
                        await c.message.answer(f"Введите все поля в /settings")

    """To delete product from cart"""

    for p in mongo.show_history(c.from_user.id):
        if c.data == f'delete {p["product"]}':
            try:
                mongo.delete_history(c.from_user.id, p["product"])
                await c.message.answer(f'Товар успешно удален (<strong>{p["product"]}</strong>) ❎', parse_mode='html')
            except IndexError:
                mongo.delete_history(c.from_user.id, mongo.show_history(c.from_user.id))
                await c.message.answer(f"Товар успешно удален ❎", parse_mode='html')

    """Return to the catalog"""

    if c.data == "back":
        mark1 = types.InlineKeyboardMarkup(row_width=True)
        for i in mongo.show_categories():
            mark1.row(types.InlineKeyboardButton(text=i['title'], callback_data=i['title']))
        mark1.add(types.InlineKeyboardButton(text="🏠", callback_data="home"))
        await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text=f"Категории товаров:", reply_markup=mark1)

    """Return to the main menu"""

    if c.data == 'home':
        mark1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mark1.row("Настройки 📎", "Помощь ❓")
        mark1.row("Заказы 📦", "Каталог 🛒")
        mark1.row("Корзина 🛍", "О нас ❕")
        await c.message.answer(f"Привет {c.message.from_user.first_name} 😁\n<strong>Это телеграмм бот магазина ЮХУ</strong>\nЗдесь ты сможешь купить нужный тебе товар и забрать его в ближайшем нашем магазине\nCreator: @YungHellen", parse_mode="html", reply_markup=mark1)

"""Callbacks of all ReplyButtons"""

@db.message_handler(content_types=['text'], state=None)
async def keyboardbutton(message: types.Message):
    if message.chat.type == 'private':
         if message.text == 'Помощь ❓':
             await message.answer(f"/start или /help - <strong>Главное меню</strong>\n/settings - <strong>Настройки</strong>\n/catalog - <strong>Каталог</strong>\n/about - <strong>О нас</strong>\n/cart - <strong>Корзина</strong>\n/history - <strong>История покупок</strong>\n\nВыберите ниже раздел справки и получите краткую помощь. Если Ваш вопрос не решен, обратитесь за помощью к живому оператору @YungHellen.", parse_mode='html')
         if message.text == 'Настройки 📎':
             mark1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
             btn1 = types.KeyboardButton(text="🏠")
             mark1.row("Имя", "Номер", "Возраст")
             mark1.row('⬅️')
             mark1.add(btn1)
             try:
                 if int(mongo.show_users(message.from_user.id)["age"]) < 18:
                     await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {mongo.show_users(message.from_user.id)['name']}\nНомер - +{mongo.show_users(message.from_user.id)['number']}\nВозраст - {mongo.show_users(message.from_user.id)['age']} <strong>(меньше 18!)</strong>", reply_markup=mark1)
                 else:
                     await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {mongo.show_users(message.from_user.id)['name']}\nНомер - +{mongo.show_users(message.from_user.id)['number']}\nВозраст - {mongo.show_users(message.from_user.id)['age']}", reply_markup=mark1)
             except TypeError and KeyError:
                 await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - не введено\nНомер - не введено\nВозраст - не введено\n\nЧтобы поля стали видны нужно заполнить их всех", reply_markup=mark1)
         if message.text == '⬅️':
             mark1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
             btn1 = types.KeyboardButton(text="🏠")
             mark1.row("Имя", "Номер", "Возраст")
             mark1.row('⬅️')
             mark1.add(btn1)
             try:
                 if int(mongo.show_users(message.from_user.id)["age"]) < 18:
                     await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {mongo.show_users(message.from_user.id)['name']}\nНомер - +{mongo.show_users(message.from_user.id)['number']}\nВозраст - {mongo.show_users(message.from_user.id)['age']} <strong>(меньше 18!)</strong>", reply_markup=mark1)
                 else:
                     await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {mongo.show_users(message.from_user.id)['name']}\nНомер - +{mongo.show_users(message.from_user.id)['number']}\nВозраст - {mongo.show_users(message.from_user.id)['age']}", reply_markup=mark1)
             except TypeError and KeyError:
                 await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - не введено\nНомер - не введено\nВозраст - не введено\n\nЧтобы поля стали видны нужно заполнить их всех", reply_markup=mark1)
         if message.text == "Корзина 🛍":
             if mongo.show_history(message.from_user.id):
                 result = 0
                 count = 0
                 for i in mongo.show_history(message.from_user.id):
                     mark3 = types.InlineKeyboardMarkup(row_width=1)
                     mark3.add(types.InlineKeyboardButton(text=f"❌", callback_data=f"delete {i['product']}"))
                     await message.answer(f"<strong>Название: </strong>{i['product']}\n<strong>Описание: </strong>{i['description']}\n<strong>Цена:</strong> {i['price']}", reply_markup=mark3)
                     result += int(i['price'])
                     count += 1
                 mark2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 mark2.row(f"Купить всё", "Обновить")
                 mark2.row(f"🏠")
                 await message.answer(f"Корзина ({count}) & Общая сумма <strong>{result} руб.</strong>", reply_markup=mark2, parse_mode='html')
             else:
                 await message.answer("Корзина пуста 🚫\nПосмотрите наш /catalog")
         if message.text == "🛍":
             if mongo.show_history(message.from_user.id):
                 result = 0
                 count = 0
                 for i in mongo.show_history(message.from_user.id):
                     mark3 = types.InlineKeyboardMarkup(row_width=1)
                     mark3.add(types.InlineKeyboardButton(text=f"❌", callback_data=f"delete {i['product']}"))
                     await message.answer(f"<strong>Название: </strong>{i['product']}\n<strong>Описание: </strong>{i['description']}\n<strong>Цена:</strong> {i['price']}", reply_markup=mark3)
                     result += int(i['price'])
                     count += 1
                 mark2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 mark2.row(f"Купить всё", "Обновить")
                 mark2.row(f"🏠")
                 await message.answer(f"Корзина ({count}) & Общая сумма <strong>{result} руб.</strong>", reply_markup=mark2, parse_mode='html')
             else:
                 await message.answer("Корзина пуста 🚫\nПосмотрите наш /catalog")
         if message.text == "Обновить":
             if mongo.show_history(message.from_user.id):
                 result = 0
                 count = 0
                 for i in mongo.show_history(message.from_user.id):
                     mark3 = types.InlineKeyboardMarkup(row_width=1)
                     mark3.add(types.InlineKeyboardButton(text=f"❌", callback_data=f"delete {i['product']}"))
                     await message.answer(f"<strong>Название: </strong>{i['product']}\n<strong>Описание: </strong>{i['description']}\n<strong>Цена:</strong> {i['price']}", reply_markup=mark3)
                     result += int(i['price'])
                     count += 1
                 mark2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 mark2.row(f"Купить всё", "Обновить")
                 mark2.row(f"🏠")
                 await message.answer(f"Корзина ({count}) & Общая сумма <strong>{result} руб.</strong>", reply_markup=mark2, parse_mode='html')
             else:
                 await message.answer("Корзина пуста 🚫\nПосмотрите наш /catalog")
         if message.text == "О нас ❕":
             await message.answer("Магазин тобачной продукции ЮХУ\nНаши магазины находятся в Владивостоке, Хабаровске, Сахалине, Улан-Удэ и Магадане\n\n<strong>Владивосток</strong>: ул. Луговая, 18; ул. Семёновская, 23\n<strong>Южно-Сахалинск</strong>: ул. Комсомольская, 157; ул.Пуркаева, 65\n<strong>Хабаровск</strong>: Амурский Бульвар 56\n<strong>Корсаков</strong>: ул.Корсаковская, 10\n<strong>Улан-Удэ</strong>: ул.Ербанова, 20; ул.Терешкова, 14\n<strong>Магадан</strong>: Проспект Карла Маркса, 23")
         if message.text == '🏠':
             mark1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
             mark1.row("Настройки 📎", "Помощь ❓")
             mark1.row("Заказы 📦", "Каталог 🛒")
             mark1.row("Корзина 🛍", "О нас ❕")
             await message.answer(f"Привет {message.from_user.first_name} 😁\n<strong>Это телеграмм бот магазина ЮХУ</strong>\nЗдесь ты сможешь купить нужный тебе товар и забрать его в ближайшем нашем магазине\nCreator: @YungHellen", parse_mode="html", reply_markup=mark1)
         if message.text == 'Имя':
             await FSMSettings.name.set()
             await message.answer("Введи свое имя")
         if message.text == 'Номер':
             await FSMSettings.number.set()
             await message.answer("Введи свой номер")
         if message.text == 'Возраст':
             await FSMSettings.age.set()
             await message.answer("Введите свой возраст")
         if message.text == 'Каталог 🛒':
             mark1 = types.InlineKeyboardMarkup(row_width=True)
             for i in mongo.show_categories():
                 mark1.row(types.InlineKeyboardButton(text=i["title"], callback_data=i["title"]))
             mark1.add(types.InlineKeyboardButton(text="🏠", callback_data="home"))
             await message.answer(f"Категории товаров:", reply_markup=mark1)
         if message.text == '🛒':
             mark1 = types.InlineKeyboardMarkup(row_width=True)
             for i in mongo.show_categories():
                 mark1.row(types.InlineKeyboardButton(text=i["title"], callback_data=i["title"]))
             mark1.add(types.InlineKeyboardButton(text="🏠", callback_data="home"))
             await message.answer(f"Категории товаров:", reply_markup=mark1)
         if message.text == "Купить всё":
             try:
                if int(mongo.show_users(message.from_user.id)['age']) < 18:
                   await message.answer("Лицам младше 18 лет продажа тобачной продукции запрещена ⛔️")
                else:
                    for i in mongo.show_history(message.from_user.id):
                        mongo.inster_cart(message.from_user.id, mongo.show_users(message.from_user.id)["name"], mongo.show_users(message.from_user.id)["number"], mongo.show_users(message.from_user.id)["age"], i["product"], i["price"])
                    mongo.delete_all_history(message.from_user.id)
                    await message.answer(f"<strong>Все товары успешно куплены</strong> ✅\nВы сможете забрать все товары в наших магазинах /about, просто показав track-номер\n<strong>Спасибо за покупку</strong> 😃", parse_mode="html")
             except TypeError and KeyError:
                 await message.answer("Заполните все поля в /settings")
         if message.text == 'Заказы 📦':
             if mongo.show_cart(message.from_user.id):
                 for i in mongo.show_cart(message.from_user.id):
                     await message.answer(f'Товар - <strong>{i["product"]}</strong>\nСтатус доставки - <strong>{i["status"]}</strong>\nTrack - <strong>{i["track"]}</strong>\n\n', parse_mode='html')
             else:
                 await message.answer(f'Вы ничего у нас не заказывали 😁\nПосмотрите наш /catalog')

if __name__ == '__main__':
    executor.start_polling(db, skip_updates=True)