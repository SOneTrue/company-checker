from aiogram.dispatcher.filters.state import StatesGroup, State


class Name(StatesGroup):
    send_name = State()
    send_group = State()
