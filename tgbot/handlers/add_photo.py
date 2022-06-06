from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from tgbot.misc.states import Name


async def user_photo_fuel(message: Message, state: FSMContext):
    await message.answer(f'Готово')
    await state.finish()


def register_photo(dp: Dispatcher):
    dp.register_message_handler(user_photo_fuel, state=Name.send_photo_fuel, content_types=types.ContentTypes.PHOTO)
