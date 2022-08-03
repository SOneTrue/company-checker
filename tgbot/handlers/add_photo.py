from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.config import load_config
from tgbot.handlers.add_info import user_info_back
from tgbot.keyboards.reply import answer_day
from tgbot.misc.album import make_album
from tgbot.misc.states import Name
from tgbot.models.users import update_info_user

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


# Фото выезд.


async def user_fuel(message: Message, state: FSMContext):
    if message.text == '/start':
        await message.answer("Вы начали заново - введите Фамилию, Имя и Отчество для дальнейшей работы.")
        await Name.send_name.set()
    else:
        photo_one = message.photo[0].file_id
        await state.update_data(photo_one=photo_one)
        await message.answer(f'✅Фото датчика топлива загружен.\n'
                             f'Загрузите фото авто, <b>вид спереди.</b>')
        await Name.send_auto_front.set()


async def user_auto_front(message: Message, state: FSMContext):
    if message.text == '/start':
        await message.answer("Вы начали заново - введите Фамилию, Имя и Отчество для дальнейшей работы.")
        await Name.send_name.set()
    else:
        photo_two = message.photo[0].file_id
        await state.update_data(photo_two=photo_two)
        await message.answer(f'✅Фото авто, вид спереди загружен.\n'
                             f'Загрузите фото авто, <b>вид сзади.</b>')
        await Name.send_auto_back.set()


async def user_auto_back(message: Message, state: FSMContext):
    if message.text == '/start':
        await message.answer("Вы начали заново - введите Фамилию, Имя и Отчество для дальнейшей работы.")
        await Name.send_name.set()
    else:
        photo_three = message.photo[0].file_id
        await state.update_data(photo_three=photo_three)
        await message.answer(f'✅Фото авто, вид сзади загружен.\n'
                             f'Загрузите фото авто, <b>вид слева.</b>')
        await Name.send_auto_left.set()


async def user_auto_left(message: Message, state: FSMContext):
    if message.text == '/start':
        await message.answer("Вы начали заново - введите Фамилию, Имя и Отчество для дальнейшей работы.")
        await Name.send_name.set()
    else:
        photo_four = message.photo[0].file_id
        await state.update_data(photo_four=photo_four)
        await message.answer(f'✅Фото авто, вид слева загружен.\n'
                             f'Загрузите фото авто, <b>вид справа.</b>')
        await Name.send_auto_right.set()


async def user_auto_right(message: Message, state: FSMContext):
    user_data = await state.get_data()
    real_name = user_data['real_name']
    number_auto = user_data['number_auto']
    road_list = user_data['road_list']
    odometer = user_data['odometer']
    comments_user = user_data['comments_user']
    if message.text == '/start':
        await message.answer("Вы начали заново - введите Фамилию, Имя и Отчество для дальнейшей работы.")
        await Name.send_name.set()
    else:
        photo_five = message.photo[0].file_id
        await state.update_data(photo_five=photo_five)
        await message.answer(f'✅ Благодарим за заполнение отчета, хорошего дня! \n'
                             f'Чтобы начать заполнения данных на вечер, нажмите /evening')
        text_user = f'{real_name} начал рейс на автомобиле {number_auto}, путевой номер {road_list}, ' \
                    f'одометр на выезд {odometer}, комментарий {comments_user}.'
        await bot.send_message(chat_id=config.tg_bot.group, text=text_user)
        await Name.start_close_day.set()


# Фото заезд.

async def user_fuel_back(message: Message, state: FSMContext):
    if message.text:
        await message.answer(f'Отправлен текст, необходимо фото, повторите отправку фото!')
        await Name.send_fuel_back.set()
    else:
        photo_six = message.photo[0].file_id
        await state.update_data(photo_six=photo_six)
        await message.answer(
            f'Оставьте комментарий, если были выявлены неисправности в течении дня или нажмите кнопку "Нет".',
            reply_markup=answer_day)
        telegram_id = message.from_user.id
        user_data = await state.get_data()
        real_name = user_data['real_name']
        number_auto = user_data['number_auto']
        road_list = user_data['road_list']
        odometer = user_data['odometer']
        odometer_back = user_data['odometer_back']
        litre_back = user_data['litre_back']
        await update_info_user(telegram_id=telegram_id, real_name=real_name, number_auto=number_auto,
                               road_list=road_list, odometer=odometer,
                               odometer_back=odometer_back, litre_back=litre_back)
        await Name.new_day.set()


async def new_day(message: Message, state: FSMContext):
    # Текст с данными.
    data = await rname_user(telegram_id=message.from_user.id)
    real_name = ''.join(data)
    user_data = await state.get_data()
    number_auto = user_data['number_auto']
    road_list = user_data['road_list']
    odometer_back = user_data['odometer_back']
    litre_back = user_data['litre_back']
    if message.text == 'Нет':
        reply_markup = types.ReplyKeyboardRemove()
        album = await make_album(state)
        await bot.send_media_group(chat_id=config.tg_bot.group, media=album)
        text = f'✅ Комментарий успешно отправлен! \n' \
               f'Благодарим за заполнения отчета, хорошего отдыха! \n' \
               f'Чтобы начать новый день нажмите на --> /start'
        await message.answer(text=text, reply_markup=reply_markup)
        text_user = f'{real_name} закончил рейс на автомобиле {number_auto}, путевой номер {road_list}, одометр на заезд ' \
                    f'{odometer_back}, количество литров - {litre_back}, комментариев нет.'
        await bot.send_message(chat_id=config.tg_bot.group, text=text_user)
        await state.reset_state(with_data=False)
    elif message.text and not message.text == '/evening':
        reply_markup = types.ReplyKeyboardRemove()
        text = f'✅ Комментарий успешно отправлен! \n' \
               f'Благодарим за заполнения отчета, хорошего отдыха! \n' \
               f'Чтобы начать новый день нажмите на --> /start'
        await message.answer(text=text, reply_markup=reply_markup)
        album = await make_album(state)
        await bot.send_media_group(chat_id=config.tg_bot.group, media=album)
        text_user = f'{real_name} закончил рейс на автомобиле {number_auto}, путевой номер {road_list}, одометр на заезд ' \
                    f'{odometer_back}, количество литров - {litre_back}, комментарий {message.text}.'
        await bot.send_message(chat_id=config.tg_bot.group, text=text_user)
        await state.reset_state(with_data=False)
    else:
        await user_info_back(message, state)


def register_photo(dp: Dispatcher):
    dp.register_message_handler(user_fuel, content_types=types.ContentTypes.PHOTO, state=Name.send_fuel)
    dp.register_message_handler(user_fuel, commands=['start'], state=Name.send_fuel)
    dp.register_message_handler(user_auto_front, content_types=types.ContentTypes.PHOTO, state=Name.send_auto_front)
    dp.register_message_handler(user_auto_front, commands=['start'], state=Name.send_auto_front)
    dp.register_message_handler(user_auto_back, content_types=types.ContentTypes.PHOTO, state=Name.send_auto_back)
    dp.register_message_handler(user_auto_back, commands=['start'], state=Name.send_auto_back)
    dp.register_message_handler(user_auto_left, content_types=types.ContentTypes.PHOTO, state=Name.send_auto_left)
    dp.register_message_handler(user_auto_left, commands=['start'], state=Name.send_auto_left)
    dp.register_message_handler(user_auto_right, content_types=types.ContentTypes.PHOTO, state=Name.send_auto_right)
    dp.register_message_handler(user_auto_right, commands=['start'], state=Name.send_auto_right)
    dp.register_message_handler(user_fuel_back, content_types=types.ContentTypes.PHOTO, state=Name.send_fuel_back)
    dp.register_message_handler(user_fuel_back, content_types=types.ContentTypes.TEXT, state=Name.send_fuel_back)
    dp.register_message_handler(new_day, state=Name.new_day)
