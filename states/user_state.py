from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    login = State()
    password = State()
    email = State()
