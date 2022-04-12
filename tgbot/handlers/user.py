from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.keyboards.reply import start_default


async def user_start(message: Message):
    await message.reply("Hello, user!", reply_markup=start_default)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
