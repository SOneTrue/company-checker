from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.config import load_config
from tgbot.filters.button_filter import Button
from tgbot.keyboards.inline import accept_keyboard
from tgbot.misc.states import Name
from tgbot.models.users import User
from tgbot.services.database import create_db_session


async def start_db():
    config = load_config()
    session_maker = await create_db_session(config)
    return session_maker


async def user_start(message: Message, user: User):
    await message.reply("Здравствуйте, введите ФИО для дальнейшей работы с ботом")
    await Name.send_name.set()


async def state_name(message: Message, state: FSMContext, user: User):
    answer = message.text
    await message.send_copy(-1001709967985, reply_markup=accept_keyboard)
    await state.finish()
    await message.answer(f'Вы ввели {answer}')


async def inline_accept(call: CallbackQuery, user: User):
    await call.message.answer('Ok')
    answer = call.message.text
    await call.message.forward(user.telegram_id)
    await user.update_user(session_maker=await start_db(), updated_fields={'real_name': answer})


async def inline_cancel(call: CallbackQuery):
    await call.message.answer('Bad')


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_message_handler(state_name, state=Name.send_name)
    dp.register_callback_query_handler(inline_accept, Button('accept'))
    dp.register_callback_query_handler(inline_cancel, Button('cancel'))
