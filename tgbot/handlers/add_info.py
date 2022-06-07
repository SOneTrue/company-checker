from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from tgbot.misc.states import Name
from tgbot.models.users import get_info_user


# Выезд.

async def user_info(message: Message):
    data = await get_info_user(telegram_id=message.from_user.id)
    real_name = ''.join(data)
    await message.answer(f"Ваше имя: {real_name}")
    await message.answer(f'Введите государственный номер авто. транспорта.')
    await Name.send_number_auto.set()


async def user_number(message: Message):
    await message.answer(f'Гос. номер введён. \n'
                         f'Введите номер путевого листа')
    await Name.send_road_list.set()


async def user_road_list(message: Message):
    await message.answer(f'Путевой лист готов \n'
                         f'Одометр на выезд')
    await Name.send_odometer.set()


async def user_odometer(message: Message):
    await message.answer(f'Одометр готов \n'
                         f'Отравьте фото датчика топлива.')
    await Name.send_fuel.set()


# Заезд.


async def user_info_back(message: Message):
    data = await get_info_user(telegram_id=message.from_user.id)
    real_name = ''.join(data)
    await message.answer(f"Ваше имя: {real_name}\n"
                         f"Ваш гос. знак - .\n"
                         f"Введите одометр на заезд")
    await Name.send_odometer_back.set()


async def user_odometer_back(message: Message):
    await message.answer(f"Одометр введён.\n"
                         f"Введите одометр на заезд")
    await Name.send_litre_back.set()


async def user_litre_back(message: Message):
    await message.answer(f"Литры на заезд введены.\n"
                         f"Отправьте фото датчика топлива на заезд!")
    await Name.send_fuel_back.set()


def register_info(dp: Dispatcher):
    dp.register_message_handler(user_info, commands=["open"])
    dp.register_message_handler(user_number, state=Name.send_number_auto)
    dp.register_message_handler(user_road_list, state=Name.send_road_list)
    dp.register_message_handler(user_odometer, state=Name.send_odometer)
    dp.register_message_handler(user_info_back, commands=["close"])
    dp.register_message_handler(user_odometer_back, state=Name.send_odometer_back)
    dp.register_message_handler(user_litre_back, state=Name.send_litre_back)
