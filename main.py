
# Modules

from dispacher import db, bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, executor
from rich.console import Console

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
    btn1 = types.KeyboardButton(text="Настройки 📎")
    btn2 = types.KeyboardButton(text="Помощь ❓")
    btn3 = types.KeyboardButton(text="Каталог 🛒")
    mark1.add(btn1, btn2, btn3)
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
    btn1 = types.KeyboardButton(text="Главная")
    mark1.row("Имя", "Номер", "Возраст")
    mark1.row('⬅️')
    mark1.add(btn1)
    try:
        if dp.show_age(message.from_user.id)[0] < 18:
            await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {dp.show_name(message.from_user.id)[0]}\nНомер - {dp.show_number(message.from_user.id)[0]}\nВозраст - {dp.show_age(message.from_user.id)[0]} <strong>(меньше 18!)</strong>", reply_markup=mark1)
        else:
            await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {dp.show_name(message.from_user.id)[0]}\nНомер - {dp.show_number(message.from_user.id)[0]}\nВозраст - {dp.show_age(message.from_user.id)[0]}", reply_markup=mark1)
    except TypeError:
        await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - не введено\nНомер - не введено\nВозраст - не введено", reply_markup=mark1)

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
                    mark2.add(types.InlineKeyboardButton(text=f"Купить за {dp.show_product(dp.show_under_categories(dp.show_categories()[i][0])[n][0])[f][3]} руб.", callback_data=dp.show_product(dp.show_under_categories(dp.show_categories()[i][0])[n][0])[f][3]))
                    await c.message.answer(f"<strong>Название: </strong>{dp.show_product(dp.show_under_categories(dp.show_categories()[i][0])[n][0])[f][1]}\n<strong>Описание: </strong>{dp.show_product(dp.show_under_categories(dp.show_categories()[i][0])[n][0])[f][2]}", reply_markup=mark2)
    if c.data == "back":
        mark1 = types.InlineKeyboardMarkup(row_width=len(dp.show_categories()))
        for i in range(0, len(dp.show_categories())):
            mark1.row(types.InlineKeyboardButton(text=dp.show_categories()[i][0], callback_data=dp.show_categories()[i][0]))
        mark1.add(types.InlineKeyboardButton(text="🏠", callback_data="home"))
        await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text=f"Категории товаров:", reply_markup=mark1)
    if c.data == 'home':
        mark1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text="Настройки 📎")
        btn2 = types.KeyboardButton(text="Помощь ❓")
        btn3 = types.KeyboardButton(text="Каталог 🛒")
        mark1.add(btn1, btn2, btn3)
        await c.message.answer(f"Привет {c.message.from_user.first_name} 😁\n<strong>Это телеграмм бот магазина ЮХУ в городе Хабаровск</strong>\nЗдесь ты сможешь купить нужный тебе товар и забрать его в ближайшем нашем магазине\nCreator: @YungHellen", parse_mode="html", reply_markup=mark1)

@db.message_handler(content_types=['text'], state=None)
async def keyboardbutton(message: types.Message):
    if message.chat.type == 'private':
         if message.text == 'Помощь ❓':
             await message.answer(f"/start или /help - <strong>Главное меню</strong>\n/settings - <strong>Настройки</strong>\n/catalog - <strong>Каталог</strong>\n\nВыберите ниже раздел справки и получите краткую помощь. Если Ваш вопрос не решен, обратитесь за помощью к живому оператору @YungHellen.", parse_mode='html')
         if message.text == 'Настройки 📎':
             mark1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
             btn1 = types.KeyboardButton(text="🏠")
             mark1.row("Имя", "Номер", "Возраст")
             mark1.row('⬅️')
             mark1.add(btn1)
             try:
                 if dp.show_age(message.from_user.id)[0] < 18:
                     await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {dp.show_name(message.from_user.id)[0]}\nНомер - {dp.show_number(message.from_user.id)[0]}\nВозраст - {dp.show_age(message.from_user.id)[0]} <strong>(меньше 18!)</strong>", reply_markup=mark1)
                 else:
                     await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {dp.show_name(message.from_user.id)[0]}\nНомер - {dp.show_number(message.from_user.id)[0]}\nВозраст - {dp.show_age(message.from_user.id)[0]}", reply_markup=mark1)
             except TypeError:
                 await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - не введено\nНомер - не введено\nВозраст - не введено", reply_markup=mark1)
         if message.text == '⬅️':
             mark1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
             btn1 = types.KeyboardButton(text="🏠")
             mark1.row("Имя", "Номер", "Возраст")
             mark1.row('⬅️')
             mark1.add(btn1)
             try:
                 if dp.show_age(message.from_user.id)[0] < 18:
                     await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {dp.show_name(message.from_user.id)[0]}\nНомер - {dp.show_number(message.from_user.id)[0]}\nВозраст - {dp.show_age(message.from_user.id)[0]} <strong>(меньше 18!)</strong>", reply_markup=mark1)
                 else:
                     await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - {dp.show_name(message.from_user.id)[0]}\nНомер - {dp.show_number(message.from_user.id)[0]}\nВозраст - {dp.show_age(message.from_user.id)[0]}", reply_markup=mark1)
             except TypeError:
                 await message.answer(f"ID - {message.from_user.id}\nИмя в telegram - {message.from_user.first_name}\nИмя - не введено\nНомер - не введено\nВозраст - не введено", reply_markup=mark1)
         if message.text == '🏠':
             mark1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
             btn1 = types.KeyboardButton(text="Настройки 📎")
             btn2 = types.KeyboardButton(text="Помощь ❓")
             btn3 = types.KeyboardButton(text="Каталог 🛒")
             mark1.add(btn1, btn2, btn3)
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

# Polling

if __name__ == '__main__':
    executor.start_polling(db, skip_updates=True)