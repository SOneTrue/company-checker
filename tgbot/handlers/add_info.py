from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.config import load_config
from tgbot.keyboards.reply import answer, number_auto_key
from tgbot.misc.form import to_control, docs
from tgbot.misc.states import Name

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


# Выезд.

async def user_info(message: Message, state: FSMContext):
    if message.text == '/morning' and message.text != '/start':
        user_data = await state.get_data()
        await message.answer(f"Ваше имя: {user_data['real_name']}")
        await message.answer(f'Выберите государственный номер авто. транспорта.', reply_markup=number_auto_key)
        await Name.send_number_auto.set()
    else:
        await message.answer("Вы начали заново - введите Фамилию, Имя и Отчество для дальнейшей работы.")
        await Name.send_name.set()


async def user_number(message: Message, state: FSMContext):
    if not message.text == '/start':
        reply_markup = types.ReplyKeyboardRemove()
        await message.answer(f'✅Гос. номер заполнен. \n'
                             f'Введите номер путевого листа.', reply_markup=reply_markup)
        await state.update_data(number_auto=message.text)
        await Name.send_road_list.set()
    else:
        await message.answer("Вы начали заново - введите Фамилию, Имя и Отчество для дальнейшей работы.")
        await Name.send_name.set()


async def user_road_list(message: Message, state: FSMContext):
    if not message.text == '/start':
        await message.answer(f'✅Путевой лист заполнен. \n'
                             f'Введите одометр на выезд.')
        await state.update_data(road_list=message.text)
        await Name.send_odometer.set()
    else:
        await message.answer("Вы начали заново - введите Фамилию, Имя и Отчество для дальнейшей работы.")
        await Name.send_name.set()


"""Чек-листы - начало """


async def user_odometer(message: Message, state: FSMContext):
    if not message.text == '/start':
        await message.answer(f'Подтвердите, что всё исправно или напишите комментарий. \n'
                             f'{to_control} \n'
                             f'{docs} \n'
                             f'<b> Если всё верно, нажмите кнопку "верно", если нет - введите комментарий! </b>',
                             reply_markup=answer)
        await state.update_data(odometer=message.text)
        await Name.send_comment.set()
    else:
        await message.answer("Вы начали заново - введите Фамилию, Имя и Отчество для дальнейшей работы.")
        await Name.send_name.set()


async def send_comment(message: Message, state: FSMContext):
    if message.text == 'Верно' and message.text != '/start':
        reply_markup = types.ReplyKeyboardRemove()
        await message.answer(f'✅ Успешно заполнены анкеты, отправьте <b>фото датчика топлива.</b>',
                             reply_markup=reply_markup)
        await state.update_data(comments_user='нет')
        await Name.send_fuel.set()
    elif message.text and message.text != '/start':
        reply_markup = types.ReplyKeyboardRemove()
        await state.update_data(comments_user=message.text)
        await message.answer(f'✅Комментарий успешно отправлен! \n'
                             f'Отправьте <b>фото датчика топлива.</b>', reply_markup=reply_markup)
        await Name.send_fuel.set()
    else:
        await message.answer("Вы начали заново - введите Фамилию, Имя и Отчество для дальнейшей работы.")
        await Name.send_name.set()


"""Конец чек-листов"""


# Заезд.


async def user_info_back(message: Message, state: FSMContext):
    try:
        user_data = await state.get_data()
        await message.answer(f"Ваше имя: {user_data['real_name']}\n"
                             f"Ваш гос. знак - {user_data['number_auto']}.\n"
                             f"Введите одометр на заезд.")
        await Name.send_odometer_back.set()
    except KeyError:
        await message.answer(f'Начните сначала, вы не заполняли данные на вечер, нажмите /start!')


async def user_odometer_back(message: Message, state: FSMContext):
    if not message.text == '/evening':
        await message.answer(f"✅Одометр заполнен.\n"
                             f"Количество заправленого топлива в литрах.")
        await state.update_data(odometer_back=message.text)
        await Name.send_litre_back.set()
    else:
        await user_info_back(message, state)


async def user_litre_back(message: Message, state: FSMContext):
    if not message.text == '/evening':
        await message.answer(f"✅Литры заполнены.\n"
                             f"Отправьте фото <b>датчика топлива</b> на заезд!")
        await state.update_data(litre_back=message.text)
        await Name.send_fuel_back.set()
    else:
        await user_info_back(message, state)


def register_info(dp: Dispatcher):
    dp.register_message_handler(user_info, commands=["morning", 'start'])
    dp.register_message_handler(user_number, state=Name.send_number_auto)
    dp.register_message_handler(user_road_list, state=Name.send_road_list)
    dp.register_message_handler(user_odometer, state=Name.send_odometer)
    dp.register_message_handler(send_comment, state=Name.send_comment)
    dp.register_message_handler(user_info_back, commands=["evening"])
    dp.register_message_handler(user_odometer_back, state=Name.send_odometer_back)
    dp.register_message_handler(user_litre_back, state=Name.send_litre_back)
