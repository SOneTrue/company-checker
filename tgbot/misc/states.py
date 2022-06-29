from aiogram.dispatcher.filters.state import StatesGroup, State


class Name(StatesGroup):
# Текстовая информация выезд
    send_name = State()
    start_day = State()
    send_number_auto = State()
    send_road_list = State()
    send_odometer = State()
    send_comment = State()
    send_docs = State()
# Фото выезд
    send_fuel = State()
    send_auto_front = State()
    send_auto_back = State()
    send_auto_left = State()
    send_auto_right = State()
# Текстовая информация заезд
    send_odometer_back = State()
    send_litre_back = State()
# Фото заезд
    send_fuel_back = State()
