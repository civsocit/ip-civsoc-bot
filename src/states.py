from aiogram.dispatcher.filters.state import State, StatesGroup


class Contact(StatesGroup):
    directors = State()
    redaction = State()
