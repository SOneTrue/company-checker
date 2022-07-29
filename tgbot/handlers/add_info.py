from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.config import load_config
from tgbot.filters.button_filter import Button
from tgbot.keyboards.inline import start_close
from tgbot.keyboards.reply import answer, number_auto_key
from tgbot.misc.form import to_control, docs
from tgbot.misc.states import Name
from tgbot.models.users import rname_user

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


# Выезд.

async def user_info(call: CallbackQuery):
    if not call.message.text == '/start':
        await call.message.edit_reply_markup()
        await call.message.delete()
        data = await rname_user(telegram_id=call.from_user.id)
        real_name = ''.join(data)
        await call.message.answer(f"Ваше имя: {real_name}")
        await call.message.answer(f'Выберите государственный номер авто. транспорта.', reply_markup=number_auto_key)
        await Name.send_number_auto.set()
    else:
        await call.message.answer("Вы начали заново - введите Фамилию, Имя и Отчество для дальнейшей работы.")
        await Name.send_name.set()


async def user_number(message: Message, state: FSMContext):
    if not message.text == '/start':
        reply_markup = types.ReplyKeyboardRemove()
        await message.answer(f'✅Гос. номер заполнен. \n'
                             f'Введите номер путевого листа.', reply_markup=reply_markup)
        number_auto = message.text
        await state.update_data(number_auto=number_auto)
        await Name.send_road_list.set()
    else:
        await message.answer("Вы начали заново - введите Фамилию, Имя и Отчество для дальнейшей работы.")
        await Name.send_name.set()


async def user_road_list(message: Message, state: FSMContext):
    if not message.text == '/start':
        await message.answer(f'✅Путевой лист заполнен. \n'
                             f'Введите одометр на выезд.')
        road_list = message.text
        await state.update_data(road_list=road_list)
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
        odometer = message.text
        await state.update_data(odometer=odometer)
        await Name.send_comment.set()
    else:
        await message.answer("Вы начали заново - введите Фамилию, Имя и Отчество для дальнейшей работы.")
        await Name.send_name.set()


async def send_comment(message: Message, state: FSMContext):
    if message.text == 'Верно' and message.text != '/start':
        reply_markup = types.ReplyKeyboardRemove()
        await message.answer(f'✅ Успешно заполнены анкеты, отправьте <b>фото датчика топлива.</b>',
                             reply_markup=reply_markup)
        comments_user = 'нет'
        await state.update_data(comments_user=comments_user)
        await Name.send_fuel.set()
    elif message.text and message.text != '/start':
        reply_markup = types.ReplyKeyboardRemove()
        comments_user = message.text
        await state.update_data(comments_user=comments_user)
        await message.answer(f'✅Комментарий успешно отправлен! \n'
                             f'Отправьте <b>фото датчика топлива.</b>', reply_markup=reply_markup)
        await Name.send_fuel.set()
    else:
        await message.answer("Вы начали заново - введите Фамилию, Имя и Отчество для дальнейшей работы.")
        await Name.send_name.set()


"""Конец чек-листов"""


# Заезд.


async def user_info_back(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.delete()
    data = await rname_user(telegram_id=call.from_user.id)
    real_name = ''.join(data)
    user_data = await state.get_data()
    number_auto = user_data['number_auto']
    await call.message.answer(f"Ваше имя: {real_name}\n"
                              f"Ваш гос. знак - {number_auto}.\n"
                              f"Введите одометр на заезд.")
    await Name.send_odometer_back.set()


async def user_odometer_back(message: Message, state: FSMContext):
    if not message.text == '/edit':
        await message.answer(f"✅Одометр заполнен.\n"
                             f"Количество заправленого топлива в литрах.")
        odometer_back = message.text
        await state.update_data(odometer_back=odometer_back)
        await Name.send_litre_back.set()
    else:
        await message.answer(f'Чтобы поменять данные вечер, нажмите кнопку!', reply_markup=start_close)
        await state.reset_state(with_data=False)


async def user_litre_back(message: Message, state: FSMContext):
    if not message.text == '/edit':
        await message.answer(f"✅Литры заполнены.\n"
                             f"Отправьте фото <b>датчика топлива</b> на заезд!")
        litre_back = message.text
        await state.update_data(litre_back=litre_back)
        await Name.send_fuel_back.set()
    else:
        await message.answer(f'Чтобы поменять данные вечер, нажмите кнопку!', reply_markup=start_close)
        await state.reset_state(with_data=False)


def register_info(dp: Dispatcher):
    dp.register_callback_query_handler(user_info, Button('exit'), state=Name.start_day)
    dp.register_message_handler(user_number, state=Name.send_number_auto)
    dp.register_message_handler(user_road_list, state=Name.send_road_list)
    dp.register_message_handler(user_odometer, state=Name.send_odometer)
    dp.register_message_handler(send_comment, state=Name.send_comment)
    dp.register_callback_query_handler(user_info_back, Button('close'))
    dp.register_message_handler(user_odometer_back, state=Name.send_odometer_back)
    dp.register_message_handler(user_litre_back, state=Name.send_litre_back)
