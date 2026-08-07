from aiogram.dispatcher.filters.state import State, StatesGroup


class ProfileStates(StatesGroup):
    name = State()
    number = State()
    age = State()
