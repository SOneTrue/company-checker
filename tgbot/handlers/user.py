from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from tgbot.misc.states import Name
from tgbot.models.users import update_user, delete_info
from tgbot.services.writer_excel import write_info
from datetime import date

async def user_start(message: Message):
    await message.answer("Здравствуйте, введите ФИО для дальнейшей работы с ботом")
    await Name.send_name.set()


async def add_user_name(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    rname = message.text
    await update_user(telegram_id=telegram_id, rname=rname)
    await message.answer('<b>Имя добавлено</b>')
    await state.finish()


async def user_save(message: Message):
    await write_info()
    await message.answer(f'Good')
    await delete_info()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_message_handler(add_user_name, state=Name.send_name)
    dp.register_message_handler(user_save, commands=["save"])
