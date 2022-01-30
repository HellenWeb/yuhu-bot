
# Modules

from dispacher import db, bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, executor
from rich.console import Console
from pymongo import MongoClient

# Class State

class FSMSettings(StatesGroup):
    name = State()
    number = State()
    age = State()

# Default Variebles

console = Console()

# Logic

@db.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    mark1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark1.row("Настройки 📎", "Помощь ❓")
    mark1.row("Заказы 📦", "Каталог 🛒")
    mark1.row("Корзина 🛍", "О нас ❕")
    await message.answer(f"Привет {message.from_user.first_name} 😁\n<strong>Это телеграмм бот магазина ЮХУ в городе Хабаровск</strong>\nЗдесь ты сможешь купить нужный тебе товар и забрать его в ближайшем нашем магазине\nCreator: @YungHellen", parse_mode="html", reply_markup=mark1)

@db.message_handler(state=FSMSettings.name)
async def upload_name(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Имя сохранено')
    if dp.show_number(message.from_user.id):
        dp.update_name(message.from_user.id, data['name'])
    else:
        dp.inster_name(message.from_user.id, data['name'])
    await state.finish()

@db.message_handler(commands=['settings'])
async def settings(message: types.Message):
    mark1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text="🏠")
    mark1.row("Имя", "Номер", "Возраст")
    mark1.row('⬅️')
    mark1.add(btn1)
    try:
        if dp.show_age(message.from_user.id)[0] < 18:
            await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {dp.show_name(message.from_user.id)[0]}\nНомер - +{dp.show_number(message.from_user.id)[0]}\nВозраст - {dp.show_age(message.from_user.id)[0]} <strong>(меньше 18!)</strong>", reply_markup=mark1)
        else:
            await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {dp.show_name(message.from_user.id)[0]}\nНомер - +{dp.show_number(message.from_user.id)[0]}\nВозраст - {dp.show_age(message.from_user.id)[0]}", reply_markup=mark1)
    except TypeError:
        await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - не введено\nНомер - не введено\nВозраст - не введено\n\nЧтобы поля стали видны нужно заполнить их всех", reply_markup=mark1)

@db.message_handler(state=FSMSettings.number)
async def upload_name(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = message.text
    await message.answer('Номер сохранен')
    if dp.show_name(message.from_user.id):
        dp.update_number(message.from_user.id, data['number'])
    else:
        dp.inster_number(message.from_user.id, data['number'])
    await state.finish()

@db.message_handler(state=FSMSettings.age)
async def upload_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer('Возраст сохранен')
    if dp.show_name(message.from_user.id):
        dp.update_age(message.from_user.id, data['age'])
    else:
        dp.inster_age(message.from_user.id, data['age'])
    await state.finish()

@db.message_handler(commands=['catalog'])
async def catalog(message: types.Message):
    mark1 = types.InlineKeyboardMarkup(row_width=len(dp.show_categories()))
    for i in range(0, len(dp.show_categories())):
        mark1.row(types.InlineKeyboardButton(text=dp.show_categories()[i][0], callback_data=dp.show_categories()[i][0]))
    mark1.add(types.InlineKeyboardButton(text="🏠", callback_data="home"))
    await message.answer(f"Категории товаров:", reply_markup=mark1)

@db.message_handler(commands=['history'])
async def history(message: types.Message):
    if dp.show_cart(message.from_user.id):
        for i in range(0, len(dp.show_cart(message.from_user.id))):
            await message.answer(f'Товар - <strong>{dp.show_cart(message.from_user.id)[i][5]}</strong>\nСтатус доставки - <strong>{dp.show_cart(message.from_user.id)[i][7]}</strong>\nTrack - <strong>{dp.show_cart(message.from_user.id)[i][6]}</strong>\n\n', parse_mode='html')
    else:
        await message.answer(f'Вы ничего у нас не заказывали 😁\nПосмотрите наш /catalog')

@db.message_handler(commands=['cart'])
async def cart(message: types.Message):
    if dp.show_history(message.from_user.id):
        for i in range(0, len(dp.show_history(message.from_user.id))):
            mark1 = types.InlineKeyboardMarkup(row_width=len(dp.show_history(message.from_user.id)))
            mark1.add(types.InlineKeyboardButton(text=f"❌", callback_data=f"delete {dp.show_history(message.from_user.id)[i][2]}"))
            await message.answer(f"<strong>Название: </strong>{dp.show_history(message.from_user.id)[i][2]}\n<strong>Описание: </strong>{dp.show_history(message.from_user.id)[i][3]}\n<strong>Цена:</strong> {dp.show_history(message.from_user.id)[i][4]}", reply_markup=mark1)
        mark2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mark2.row(f"Купить всё", "Обновить")
        mark2.row(f"🏠")
        await message.answer(f"Корзина ({len(dp.show_history(message.from_user.id))})", reply_markup=mark2)
    else:
        await message.answer("Корзина пуста 🚫\nПосмотрите наш /catalog")

@db.message_handler(commands=['about'])
async def about(message: types.Message):
    await message.answer("Магазин тобачной продукции ЮХУ\nНаши магазины находятся по всему Хабаровску\nул. Карла Маркса; тогровый центр Броско Молл; ул. Ленинградская")

@db.callback_query_handler(lambda c: True)
async def catalog(c: types.CallbackQuery):
    for i in range(0, len(dp.show_categories())):
        if c.data == dp.show_categories()[i][0]:
            # await c.message.answer(dp.show_under_categories(dp.show_categories()))
            try:
                mark1 = types.InlineKeyboardMarkup(row_width=len(dp.show_under_categories(dp.show_categories()[i][0])))
                for n in range(0, len(dp.show_under_categories(dp.show_categories()[i][0]))):
                    mark1.row(types.InlineKeyboardButton(text=dp.show_under_categories(dp.show_categories()[i][0])[n][0], callback_data=dp.show_under_categories(dp.show_categories()[i][0])[n][0]))
                mark1.add(types.InlineKeyboardButton(text="⬅️", callback_data="back"))
                await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Подгруппы товаров:", reply_markup=mark1)

            except ZeroDivisionError:
                mark1 = types.InlineKeyboardMarkup(row_width=1)
                mark1.add(types.InlineKeyboardButton(text="⬅️", callback_data="back"))
                await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Подгруппы товаров:", reply_markup=mark1)
        for n in range(0, len(dp.show_under_categories(dp.show_categories()[i][0]))):
            if c.data == dp.show_under_categories(dp.show_categories()[i][0])[n][0]:
                for f in range(0, len(dp.show_product(dp.show_under_categories(dp.show_categories()[i][0])[n][0]))):
                    mark2 = types.InlineKeyboardMarkup(row_width=1)
                    mark2.add(types.InlineKeyboardButton(text=f"Добавить в корзину 🛍", callback_data=dp.show_product(dp.show_under_categories(dp.show_categories()[i][0])[n][0])[f][1]))
                    mark2.add(types.InlineKeyboardButton(text=f"Купить - {dp.show_product(dp.show_under_categories(dp.show_categories()[i][0])[n][0])[f][3]} руб.", callback_data=dp.show_product(dp.show_under_categories(dp.show_categories()[i][0])[n][0])[f][1]))
                    await c.message.answer(f"<strong>Название: </strong>{dp.show_product(dp.show_under_categories(dp.show_categories()[i][0])[n][0])[f][1]}\n<strong>Описание: </strong>{dp.show_product(dp.show_under_categories(dp.show_categories()[i][0])[n][0])[f][2]}", reply_markup=mark2)
                mark3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                mark3.row("🏠", "🛒", "🛍")
                await c.message.answer(f"Позаны все товары ({len(dp.show_product(dp.show_under_categories(dp.show_categories()[i][0])[n][0]))})", reply_markup=mark3)
        for n in range(0, len(dp.show_under_categories(dp.show_categories()[i][0]))):
            for f in range(0, len(dp.show_product(dp.show_under_categories(dp.show_categories()[i][0])[n][0]))):
                if c.data == dp.show_product(dp.show_under_categories(dp.show_categories()[i][0])[n][0])[f][1]:
                    try:
                        dp.inster_history(c.from_user.id, dp.show_product(dp.show_under_categories(dp.show_categories()[i][0])[n][0])[f][1], dp.show_product(dp.show_under_categories(dp.show_categories()[i][0])[n][0])[f][2], dp.show_product(dp.show_under_categories(dp.show_categories()[i][0])[n][0])[f][3])
                        await c.message.answer(f"Товар <strong>{dp.show_product(dp.show_under_categories(dp.show_categories()[i][0])[n][0])[f][1]}</strong> успешно добавлен в корзину", parse_mode='html')
                    except TypeError:
                        await c.message.answer(f"Введите все поля в /settings")
    for p in range(0, len(dp.show_history(c.from_user.id))):
        if c.data == f"delete {dp.show_history(c.from_user.id)[p][2]}":
            try:
                dp.delete_history(c.from_user.id, dp.show_history(c.from_user.id)[p][2])
                await c.message.answer(f"Товар успешно удален (<strong>{dp.show_history(c.from_user.id)[p][2]}</strong>) ❎", parse_mode='html')
            except IndexError:
                dp.delete_history(c.from_user.id, dp.show_history(c.from_user.id))
                await c.message.answer(f"Товар успешно удален ❎", parse_mode='html')
    if c.data == "back":
        mark1 = types.InlineKeyboardMarkup(row_width=len(dp.show_categories()))
        for i in range(0, len(dp.show_categories())):
            mark1.row(types.InlineKeyboardButton(text=dp.show_categories()[i][0], callback_data=dp.show_categories()[i][0]))
        mark1.add(types.InlineKeyboardButton(text="🏠", callback_data="home"))
        await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text=f"Категории товаров:", reply_markup=mark1)
    if c.data == 'home':
        mark1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mark1.row("Настройки 📎", "Помощь ❓")
        mark1.row("Заказы 📦", "Каталог 🛒")
        mark1.row("Корзина 🛍", "О нас ❕")
        await c.message.answer(f"Привет {c.message.from_user.first_name} 😁\n<strong>Это телеграмм бот магазина ЮХУ в городе Хабаровск</strong>\nЗдесь ты сможешь купить нужный тебе товар и забрать его в ближайшем нашем магазине\nCreator: @YungHellen", parse_mode="html", reply_markup=mark1)

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
                 if dp.show_age(message.from_user.id)[0] < 18:
                     await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {dp.show_name(message.from_user.id)[0]}\nНомер - +{dp.show_number(message.from_user.id)[0]}\nВозраст - {dp.show_age(message.from_user.id)[0]} <strong>(меньше 18!)</strong>", reply_markup=mark1)
                 else:
                     await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {dp.show_name(message.from_user.id)[0]}\nНомер - +{dp.show_number(message.from_user.id)[0]}\nВозраст - {dp.show_age(message.from_user.id)[0]}", reply_markup=mark1)
             except TypeError:
                 await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - не введено\nНомер - не введено\nВозраст - не введено\n\nЧтобы поля стали видны нужно заполнить их всех", reply_markup=mark1)
         if message.text == '⬅️':
             mark1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
             btn1 = types.KeyboardButton(text="🏠")
             mark1.row("Имя", "Номер", "Возраст")
             mark1.row('⬅️')
             mark1.add(btn1)
             try:
                 if dp.show_age(message.from_user.id)[0] < 18:
                     await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {dp.show_name(message.from_user.id)[0]}\nНомер - +{dp.show_number(message.from_user.id)[0]}\nВозраст - {dp.show_age(message.from_user.id)[0]} <strong>(меньше 18!)</strong>", reply_markup=mark1)
                 else:
                     await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {dp.show_name(message.from_user.id)[0]}\nНомер - +{dp.show_number(message.from_user.id)[0]}\nВозраст - {dp.show_age(message.from_user.id)[0]}", reply_markup=mark1)
             except TypeError:
                 await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - не введено\nНомер - не введено\nВозраст - не введено\n\nЧтобы поля стали видны нужно заполнить их всех", reply_markup=mark1)
         if message.text == "Корзина 🛍":
             if dp.show_history(message.from_user.id):
                 for i in range(0, len(dp.show_history(message.from_user.id))):
                     mark3 = types.InlineKeyboardMarkup(row_width=len(dp.show_history(message.from_user.id)))
                     mark3.add(types.InlineKeyboardButton(text=f"❌", callback_data=f"delete {dp.show_history(message.from_user.id)[i][2]}"))
                     await message.answer(f"<strong>Название: </strong>{dp.show_history(message.from_user.id)[i][2]}\n<strong>Описание: </strong>{dp.show_history(message.from_user.id)[i][3]}\n<strong>Цена:</strong> {dp.show_history(message.from_user.id)[i][4]}", reply_markup=mark3)
                 mark2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 mark2.row(f"Купить всё", "Обновить")
                 mark2.row(f"🏠")
                 await message.answer(f"Корзина ({len(dp.show_history(message.from_user.id))})", reply_markup=mark2)
             else:
                 await message.answer("Корзина пуста 🚫\nПосмотрите наш /catalog")
         if message.text == "🛍":
             if dp.show_history(message.from_user.id):
                 for i in range(0, len(dp.show_history(message.from_user.id))):
                     mark1 = types.InlineKeyboardMarkup(row_width=len(dp.show_history(message.from_user.id)))
                     mark1.add(types.InlineKeyboardButton(text=f"❌", callback_data=f"delete {dp.show_history(message.from_user.id)[i][2]}"))
                     await message.answer(f"<strong>Название: </strong>{dp.show_history(message.from_user.id)[i][2]}\n<strong>Описание: </strong>{dp.show_history(message.from_user.id)[i][3]}\n<strong>Цена:</strong> {dp.show_history(message.from_user.id)[i][4]}", reply_markup=mark1)
                 mark2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 mark2.row(f"Купить всё", "Обновить")
                 mark2.row(f"🏠")
                 await message.answer(f"Корзина ({len(dp.show_history(message.from_user.id))})", reply_markup=mark2)
             else:
                 await message.answer("Корзина пуста 🚫\nПосмотрите наш /catalog")
         if message.text == "Обновить":
             if dp.show_history(message.from_user.id):
                 for i in range(0, len(dp.show_history(message.from_user.id))):
                     mark3 = types.InlineKeyboardMarkup(row_width=len(dp.show_history(message.from_user.id)))
                     mark3.add(types.InlineKeyboardButton(text=f"❌", callback_data=f"delete {dp.show_history(message.from_user.id)[i][2]}"))
                     await message.answer(f"<strong>Название: </strong>{dp.show_history(message.from_user.id)[i][2]}\n<strong>Описание: </strong>{dp.show_history(message.from_user.id)[i][3]}\n<strong>Цена:</strong> {dp.show_history(message.from_user.id)[i][4]}", reply_markup=mark3)
                 mark2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 mark2.row(f"Купить всё", "Обновить")
                 mark2.row(f"🏠")
                 await message.answer(f"Корзина ({len(dp.show_history(message.from_user.id))})", reply_markup=mark2)
             else:
                 await message.answer("Корзина пуста 🚫\nПосмотрите наш /catalog")
         if message.text == "О нас ❕":
             await message.answer("Магазин тобачной продукции ЮХУ\nНаши магазины находятся по всему Хабаровску\nул. Карла Маркса; тогровый центр Броско Молл; ул. Ленинградская")
         if message.text == '🏠':
             mark1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
             mark1.row("Настройки 📎", "Помощь ❓")
             mark1.row("Заказы 📦", "Каталог 🛒")
             mark1.row("Корзина 🛍", "О нас ❕")
             await message.answer(f"Привет {message.from_user.first_name} 😁\n<strong>Это телеграмм бот магазина ЮХУ в городе Хабаровск</strong>\nЗдесь ты сможешь купить нужный тебе товар и забрать его в ближайшем нашем магазине\nCreator: @YungHellen", parse_mode="html", reply_markup=mark1)
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
             mark1 = types.InlineKeyboardMarkup(row_width=len(dp.show_categories()))
             for i in range(0, len(dp.show_categories())):
                 mark1.row(types.InlineKeyboardButton(text=dp.show_categories()[i][0], callback_data=dp.show_categories()[i][0]))
             mark1.add(types.InlineKeyboardButton(text="🏠", callback_data="home"))
             await message.answer(f"Категории товаров:", reply_markup=mark1)
         if message.text == '🛒':
             mark1 = types.InlineKeyboardMarkup(row_width=len(dp.show_categories()))
             for i in range(0, len(dp.show_categories())):
                 mark1.row(types.InlineKeyboardButton(text=dp.show_categories()[i][0], callback_data=dp.show_categories()[i][0]))
             mark1.add(types.InlineKeyboardButton(text="🏠", callback_data="home"))
             await message.answer(f"Категории товаров:", reply_markup=mark1)
         if message.text == "Купить всё":
             try:
                 for i in range(0, len(dp.show_history(message.from_user.id))):
                     dp.inster_cart(message.from_user.id, dp.show_name(message.from_user.id)[0], dp.show_number(message.from_user.id)[0], dp.show_age(message.from_user.id)[0], dp.show_history(message.from_user.id)[i][2])
                 dp.delete_all_history(message.from_user.id)
                 await message.answer(f"Все товары успешно куплены ✅")
             except TypeError:
                 await message.answer("Заполните все поля в /settings")
         if message.text == 'Заказы 📦':
             if dp.show_cart(message.from_user.id):
                 for i in range(0, len(dp.show_cart(message.from_user.id))):
                     await message.answer(f'Товар - <strong>{dp.show_cart(message.from_user.id)[i][5]}</strong>\nСтатус доставки - <strong>{dp.show_cart(message.from_user.id)[i][7]}</strong>\nTrack - <strong>{dp.show_cart(message.from_user.id)[i][6]}</strong>\n\n', parse_mode='html')
             else:
                 await message.answer(f'Вы ничего у нас не заказывали 😁\nПосмотрите наш /catalog')

# Polling

if __name__ == '__main__':
    executor.start_polling(db, skip_updates=True)