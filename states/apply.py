from aiogram.dispatcher.filters.state import StatesGroup, State


class app(StatesGroup):
    name = State()
    surname = State()
    weight = State()
    contacts = State()
    photo = State()


class Name(StatesGroup):
    name = State()
    surname = State()

