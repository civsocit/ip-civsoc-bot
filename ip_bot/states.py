from aiogram.dispatcher.filters.state import State, StatesGroup


class Join(StatesGroup):
    full_name = State()
    birthday = State()
    email = State()
    fraction_charter_agree = State()
    about = State()
    is_civsoc_member = State()
    city = State()
    phone_no = State()
    civsoc_charter_agree = State()


class Contact(StatesGroup):
    directors = State()
    redaction = State()
