from aiogram.dispatcher.filters.state import State, StatesGroup


class Registr(StatesGroup):
    first_name = State()
    last_name = State()
    phone_number = State()
    school = State()
    address = State()
    profession = State()
    final_step = State()