from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from tgbot.misc.states import Name

# Фото выезд.
from tgbot.models.users import update_info_user


async def user_fuel(message: Message):
    await message.answer(f'Датчик фото загружен.\n'
                         f'Загрузите фото авто, вид спереди.')
    await Name.send_auto_front.set()


async def user_auto_front(message: Message):
    await message.answer(f'Фото авто, вид спереди загружен.\n'
                         f'Загрузите фото авто, вид сзади.')
    await Name.send_auto_back.set()


async def user_auto_back(message: Message):
    await message.answer(f'Фото авто, вид сзади загружен.\n'
                         f'Загрузите фото авто, вид слева.')
    await Name.send_auto_left.set()


async def user_auto_left(message: Message):
    await message.answer(f'Фото авто, вид слева загружен.\n'
                         f'Загрузите фото авто, вид справа.')
    await Name.send_auto_right.set()


async def user_auto_right(message: Message, state: FSMContext):
    await message.answer(f'Успешная загрузка фото на выезд.')
    await state.reset_state(with_data=False)


# Фото заезд.

async def user_fuel_back(message: Message, state: FSMContext):
    await message.answer(f'Успешная загрузка фото на заезд.')
    telegram_id = message.from_user.id
    user_data = await state.get_data()
    number_auto = user_data['number_auto']
    road_list = user_data['road_list']
    odometer = user_data['odometer']
    odometer_back = user_data['odometer_back']
    litre_back = user_data['litre_back']
    await update_info_user(telegram_id=telegram_id, number_auto=number_auto, road_list=road_list, odometer=odometer,
                           odometer_back=odometer_back, litre_back=litre_back)
    await state.reset_state(with_data=True)


def register_photo(dp: Dispatcher):
    dp.register_message_handler(user_fuel, state=Name.send_fuel, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(user_auto_front, state=Name.send_auto_front, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(user_auto_back, state=Name.send_auto_back, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(user_auto_left, state=Name.send_auto_left, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(user_auto_right, state=Name.send_auto_right, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(user_fuel_back, state=Name.send_fuel_back, content_types=types.ContentTypes.PHOTO)
