from aiogram.dispatcher.filters.state import StatesGroup, State


class Name(StatesGroup):
    send_name = State()
    send_number_auto = State()
    send_road_list = State()
    send_odometer = State()

    send_photo_fuel = State()
