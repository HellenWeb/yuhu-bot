from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.states.profile import ProfileStates
from bot.texts import (
    INVALID_AGE_RANGE_TEXT,
    INVALID_AGE_TEXT,
    PROFILE_FIELD_PROMPTS,
    PROFILE_FIELD_SAVE_TEXTS,
)


def register(dispatcher, services):
    profile = services.profile
    views = services.views

    @dispatcher.message_handler(commands=["settings"])
    async def settings_command(message):
        await views.send_settings(message)

    @dispatcher.message_handler(Text(equals=["Настройки 📎", "⬅️"]), state=None)
    async def settings_button(message):
        await views.send_settings(message)

    @dispatcher.message_handler(
        Text(equals=["Имя", "Номер", "Возраст"]),
        state=None,
    )
    async def choose_profile_field(message):
        field = {
            "Имя": "name",
            "Номер": "number",
            "Возраст": "age",
        }[message.text]
        await getattr(ProfileStates, field).set()
        await message.answer(PROFILE_FIELD_PROMPTS[field])

    @dispatcher.message_handler(state=ProfileStates.name)
    async def save_name(message, state: FSMContext):
        profile.save_name(message.from_user.id, message.text)
        await message.answer(PROFILE_FIELD_SAVE_TEXTS["name"])
        await state.finish()

    @dispatcher.message_handler(state=ProfileStates.number)
    async def save_number(message, state: FSMContext):
        profile.save_number(message.from_user.id, message.text)
        await message.answer(PROFILE_FIELD_SAVE_TEXTS["number"])
        await state.finish()

    @dispatcher.message_handler(state=ProfileStates.age)
    async def save_age(message, state: FSMContext):
        try:
            age = int(message.text)
        except (TypeError, ValueError):
            await message.answer(INVALID_AGE_TEXT)
            return

        if not 0 < age < 130:
            await message.answer(INVALID_AGE_RANGE_TEXT)
            return

        profile.save_age(message.from_user.id, age)
        await message.answer(PROFILE_FIELD_SAVE_TEXTS["age"])
        await state.finish()
