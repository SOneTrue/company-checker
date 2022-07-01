from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode


async def bot_echo(message: types.Message):
    text = [
        f'Введены неверные данные, проверьте: \n'
        f'Отправлено фото, а необходимо текст. \n'
        f'Отправлен текст, а необходимо фото.'
    ]


    await message.answer('\n'.join(text))


async def bot_echo_all(message: types.Message, state: FSMContext):
    text = [
        f'Введены неверные данные, проверьте: \n'
        f'Отправлено фото, а необходимо текст. \n'
        f'Отправлен текст, а необходимо фото.'
    ]
    await message.answer('\n'.join(text))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
