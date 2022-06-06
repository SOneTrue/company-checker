from aiogram.dispatcher.filters.state import StatesGroup, State


class Name(StatesGroup):
    send_name = State()
    send_number_auto = State()
    send_road_list = State()
    send_odometer = State()

    send_photo_fuel = State()
    send_auto_front = State()
    send_auto_back = State()
    send_auto_left = State()
    send_auto_right = State()
