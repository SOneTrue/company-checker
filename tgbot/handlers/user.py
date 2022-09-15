from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.misc.states import Name
from tgbot.models.users import delete_info, add_user
from tgbot.services.writer_excel import write_info


async def user_start(message: Message, state: FSMContext):
    await state.reset_state(with_data=True)
    await message.answer("Здравствуйте, введите Фамилию, Имя и Отчество для дальнейшей работы.")
    await Name.send_name.set()


async def add_user_name(message: Message, state: FSMContext):
    if not message.text == '/start':
        real_name = message.text
        telegram_id = message.from_user.id
        if message.from_user.username:
            await add_user(telegram_id=telegram_id, username=message.from_user.username, real_name=real_name,
                           number_auto=None, road_list=None, odometer=None, odometer_back=None, litre_back=None)
            await state.update_data(real_name=message.text)
            await message.answer(
                '<b>✅ ФИО успешно добавлено, чтобы начать заполнение информации нажмите на кнопку /morning </b>', )
            await state.reset_state(with_data=False)
        else:
            await add_user(telegram_id=telegram_id, username=None, real_name=real_name, number_auto=None,
                           road_list=None, odometer=None, odometer_back=None, litre_back=None)
            await state.update_data(real_name=message.text)
            await message.answer(
                '<b>✅ ФИО успешно добавлено, чтобы начать заполнение информации нажмите на кнопку /morning </b>', )
            await state.reset_state(with_data=False)
    else:
        await message.answer("⛔️Не верное имя или неправильно заполнено поле, повторите ввод ФИО!")
        await Name.send_name.set()


async def user_save(message: Message):
    await write_info()
    await message.answer(f'✅ Успешное сохранение таблицы в Excel!')
    await delete_info()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_message_handler(add_user_name, state=Name.send_name)
    dp.register_message_handler(user_save, commands=["save"])
