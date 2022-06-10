from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.misc.form import to_control, docs
from tgbot.misc.states import Name
from tgbot.models.users import rname_user


# Выезд.

async def user_info(message: Message):
    data = await rname_user(telegram_id=message.from_user.id)
    try:
        real_name = ''.join(data)
        await message.answer(f"Ваше имя: {real_name}")
        await message.answer(f'Введите государственный номер авто. транспорта.')
        await Name.send_number_auto.set()
    except TypeError:
        await message.answer(f'Вы не ввели своё реальное имя, начните с начала - /start')


async def user_number(message: Message, state: FSMContext):
    await message.answer(f'Гос. номер введён. \n'
                         f'Введите номер путевого листа')
    number_auto = message.text
    await state.update_data(number_auto=number_auto)
    await Name.send_road_list.set()


async def user_road_list(message: Message, state: FSMContext):
    await message.answer(f'Путевой лист готов \n'
                         f'Одометр на выезд')
    road_list = message.text
    await state.update_data(road_list=road_list)
    await Name.send_odometer.set()


async def user_odometer(message: Message, state: FSMContext):
    await message.answer(f'Одометр готов \n'
                         f'Подтвердите что всё исправно или напишите комментарий. \n'
                         f'{to_control}.')
    odometer = message.text
    await state.update_data(odometer=odometer)
    await Name.send_to_control.set()


async def user_accept_to(message: Message, state: FSMContext):
    await message.answer(f'Тех. контроль готово. \n'
                         f'Подтвердите что всё исправно или напишите комментарий. \n'
                         f'{docs}.')
    await Name.send_docs.set()

async def user_accept_docs(message: Message, state: FSMContext):
    await message.answer(f'Успешно заполнены анкеты, пришлите фото датчика топлива')
    await Name.send_fuel.set()


# Заезд.


async def user_info_back(message: Message, state: FSMContext):
    data = await rname_user(telegram_id=message.from_user.id)
    try:
        real_name = ''.join(data)
        user_data = await state.get_data()
        number_auto = user_data['number_auto']
        await message.answer(f"Ваше имя: {real_name}\n"
                             f"Ваш гос. знак - {number_auto}.\n"
                             f"Введите одометр на заезд")
        await Name.send_odometer_back.set()
    except TypeError:
        await message.answer('Вы не заполнили информацию о себе, начните сначала - /start')
        await state.reset_state(with_data=True)


async def user_odometer_back(message: Message, state: FSMContext):
    await message.answer(f"Одометр введён.\n"
                         f"Введите одометр на заезд")
    odometer_back = message.text
    await state.update_data(odometer_back=odometer_back)
    await Name.send_litre_back.set()


async def user_litre_back(message: Message, state: FSMContext):
    await message.answer(f"Литры на заезд введены.\n"
                         f"Отправьте фото датчика топлива на заезд!")
    litre_back = message.text
    await state.update_data(litre_back=litre_back)
    await Name.send_fuel_back.set()


def register_info(dp: Dispatcher):
    dp.register_message_handler(user_info, commands=["open"])
    dp.register_message_handler(user_number, state=Name.send_number_auto)
    dp.register_message_handler(user_road_list, state=Name.send_road_list)
    dp.register_message_handler(user_odometer, state=Name.send_odometer)
    dp.register_message_handler(user_accept_to, state=Name.send_to_control)
    dp.register_message_handler(user_accept_docs, state=Name.send_docs)
    dp.register_message_handler(user_info_back, commands=["close"])
    dp.register_message_handler(user_odometer_back, state=Name.send_odometer_back)
    dp.register_message_handler(user_litre_back, state=Name.send_litre_back)
