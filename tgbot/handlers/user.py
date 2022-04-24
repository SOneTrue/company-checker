from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.inline import accept_keyboard
from tgbot.misc.states import Name
from tgbot.models.users import User


async def user_start(message: Message, user: User):
    await message.reply("Здравствуйте, введите ФИО для дальнейшей работы с ботом")
    await Name.send_name.set()


async def state_name(message: Message, state: FSMContext):
    answer = message.text
    await message.send_copy(-1001709967985, reply_markup=accept_keyboard)
    await state.finish()
    await message.answer(f'Вы ввели {answer}')


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_message_handler(state_name, state=Name.send_name)