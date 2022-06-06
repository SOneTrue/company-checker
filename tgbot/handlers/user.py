from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from tgbot.misc.states import Name
from tgbot.models.users import update_user


async def user_start(message: Message):
    await message.reply("Здравствуйте, введите ФИО для дальнейшей работы с ботом")
    await Name.send_name.set()


async def add_user_name(message: Message, state: FSMContext):
    await message.answer("Готово")
    telegram_id = message.from_user.id
    print(telegram_id)
    rname = message.text
    await update_user(telegram_id=telegram_id, rname=rname)
    await state.finish()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_message_handler(add_user_name, state=Name.send_name)
