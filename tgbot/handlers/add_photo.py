from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, MediaGroup

from tgbot.config import load_config
from tgbot.keyboards.inline import start_close
from tgbot.keyboards.reply import answer_day
from tgbot.misc.states import Name
from tgbot.models.users import update_info_user, rname_user

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


# Фото выезд.
async def user_fuel(message: Message, state: FSMContext):
    photo_one = message.photo[0].file_id
    await state.update_data(photo_one=photo_one)
    await message.answer(f'✅ Фото датчика топлива загружен.\n'
                         f'Загрузите фото авто, <b>вид спереди.</b>')
    await Name.send_auto_front.set()


async def user_auto_front(message: Message, state: FSMContext):
    photo_two = message.photo[0].file_id
    await state.update_data(photo_two=photo_two)
    await message.answer(f'✅ Фото авто, вид спереди загружен.\n'
                         f'Загрузите фото авто, <b>вид сзади.</b>')
    await Name.send_auto_back.set()


async def user_auto_back(message: Message, state: FSMContext):
    photo_three = message.photo[0].file_id
    await state.update_data(photo_three=photo_three)
    await message.answer(f'✅ Фото авто, вид сзади загружен.\n'
                         f'Загрузите фото авто, <b>вид слева.</b>')
    await Name.send_auto_left.set()


async def user_auto_left(message: Message, state: FSMContext):
    photo_four = message.photo[0].file_id
    await state.update_data(photo_four=photo_four)
    await message.answer(f'✅ Фото авто, вид слева загружен.\n'
                         f'Загрузите фото авто, <b>вид справа.</b>')
    await Name.send_auto_right.set()


async def user_auto_right(message: Message, state: FSMContext):
    photo_five = message.photo[0].file_id
    await state.update_data(photo_five=photo_five)
    await message.answer(f'✅ Благодарим за заполнение отчета, хорошего дня!', reply_markup=start_close)
    await state.reset_state(with_data=False)


# Фото заезд.

async def user_fuel_back(message: Message, state: FSMContext):
    photo_six = message.photo[0].file_id
    await state.update_data(photo_six=photo_six)
    await message.answer(
        f'Оставьте комментарий, если были выявлены неисправности в течении дня или нажмите кнопку "Нет".',
        reply_markup=answer_day)
    telegram_id = message.from_user.id
    user_data = await state.get_data()
    number_auto = user_data['number_auto']
    road_list = user_data['road_list']
    odometer = user_data['odometer']
    odometer_back = user_data['odometer_back']
    litre_back = user_data['litre_back']
    await update_info_user(telegram_id=telegram_id, number_auto=number_auto, road_list=road_list, odometer=odometer,
                           odometer_back=odometer_back, litre_back=litre_back)
    await Name.new_day.set()


async def new_day(message: Message, state: FSMContext):
    # Формирование альбома.
    album = MediaGroup()
    user_data = await state.get_data()
    photo_one = user_data['photo_one']
    photo_two = user_data['photo_two']
    photo_three = user_data['photo_three']
    photo_four = user_data['photo_four']
    photo_five = user_data['photo_five']
    photo_six = user_data['photo_six']
    album.attach_photo(photo_one)
    album.attach_photo(photo_two)
    album.attach_photo(photo_three)
    album.attach_photo(photo_four)
    album.attach_photo(photo_five)
    album.attach_photo(photo_six)
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
        await bot.send_media_group(chat_id=config.tg_bot.group, media=album)
        text = f'✅ Комментарий успешно отправлен! \n' \
               f'Благодарим за заполнения отчета, хорошего отдыха! \n' \
               f'Чтобы начать новый день нажмите на --> /start'
        await message.answer(text=text, reply_markup=reply_markup)
        text_user = f'{real_name} закончил рейс на автомобиле {number_auto}, путевой номер {road_list}, одометр на заезд ' \
                    f'{odometer_back}, количество литров - {litre_back}, комментариев нет.'
        await bot.send_message(chat_id=config.tg_bot.group, text=text_user)
    else:
        reply_markup = types.ReplyKeyboardRemove()
        text = f'✅ Комментарий успешно отправлен! \n' \
               f'Благодарим за заполнения отчета, хорошего отдыха! \n' \
               f'Чтобы начать новый день нажмите на --> /start'
        await message.answer(text=text, reply_markup=reply_markup)
        await bot.send_media_group(chat_id=config.tg_bot.group, media=album)
        text_user = f'{real_name} закончил рейс на автомобиле {number_auto}, путевой номер {road_list}, одометр на заезд ' \
                    f'{odometer_back}, количество литров - {litre_back}, комментарий {message.text}.'
        await bot.send_message(chat_id=config.tg_bot.group, text=text_user)
    await state.reset_state(with_data=True)


def register_photo(dp: Dispatcher):
    dp.register_message_handler(user_fuel, state=Name.send_fuel, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(user_auto_front, state=Name.send_auto_front, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(user_auto_back, state=Name.send_auto_back, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(user_auto_left, state=Name.send_auto_left, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(user_auto_right, state=Name.send_auto_right, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(user_fuel_back, state=Name.send_fuel_back, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(new_day, state=Name.new_day)
