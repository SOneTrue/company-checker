from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext



async def bot_echo(message: types.Message, state: FSMContext):
    text = [
        f'⛔️ Введены неверные данные, перепроверьте что требуется отправить, текст или фотографию!\n'
        f'Для того что бы начать сначала нажмите /start'
    ]

    await message.answer('\n'.join(text))


async def bot_echo_all(message: types.Message, state: FSMContext):
    text = [
        f'⛔️ Введены неверные данные, перепроверьте что требуется отправить, текст или фотографию!\n'
        f'Для того что бы начать сначала нажмите /start'
    ]
    await message.answer('\n'.join(text))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
