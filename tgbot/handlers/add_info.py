from aiogram import Dispatcher
# from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from tgbot.misc.states import Name
from tgbot.models.users import get_info_user


async def user_get_info(message: Message):
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
    await Name.send_photo_fuel.set()


def register_info(dp: Dispatcher):
    dp.register_message_handler(user_get_info, commands=["open"])
    dp.register_message_handler(user_number, state=Name.send_number_auto)
    dp.register_message_handler(user_road_list, state=Name.send_road_list)
    dp.register_message_handler(user_odometer, state=Name.send_odometer)
