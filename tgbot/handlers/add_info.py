from aiogram import Dispatcher
# from aiogram.dispatcher import FSMContext
from aiogram.types import Message
# from tgbot.misc.states import Name
from tgbot.models.users import get_info_user


async def user_start(message: Message):
    data = await get_info_user(telegram_id=message.from_user.id)
    real_name = ''.join(data)
    await message.answer(f"Ваше имя: {real_name}")


# async def add_user_name(message: Message, state: FSMContext):
#     await message.answer("Готово")
#     telegram_id = message.from_user.id
#     rname = message.text
#     await update_user(telegram_id=telegram_id, rname=rname)
#     await state.finish()


def register_info(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["open"])
