from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode


async def bot_echo(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    text = [
        f'⛔️ Введены неверные данные, начните с начала --> /start ⚙️'
    ]


    await message.answer('\n'.join(text))


async def bot_echo_all(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    text = [
        f'⛔️ Введены неверные данные, начните с начала --> /start ⚙️'
    ]
    await message.answer('\n'.join(text))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
