from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.inline import start_exit, start_close
from tgbot.misc.states import Name
from tgbot.models.users import update_user, delete_info
from tgbot.services.writer_excel import write_info


async def user_start(message: Message, state: FSMContext):
    await state.reset_state(with_data=True)
    await message.answer("Здравствуйте, введите Фамилию, Имя и Отчество для дальнейшей работы.")
    await Name.send_name.set()


async def add_user_name(message: Message, state: FSMContext):
    if not message.text == '/start':
        telegram_id = message.from_user.id
        rname = message.text
        await update_user(telegram_id=telegram_id, rname=rname)
        await message.answer('<b>✅ ФИО успешно добавлено, нажмите на кнопку чтобы начать заполнение информации! </b>',
                             reply_markup=start_exit)
        await Name.start_day.set()
    else:
        await message.answer("⛔️Не верное имя или неправильно заполнено поле, повторите ввод ФИО!")
        await Name.send_name.set()


async def user_save(message: Message):
    await write_info()
    await message.answer(f'✅ Успешное сохранение таблицы в Excel!')
    await delete_info()


async def user_edit_back(message: Message, state: FSMContext):
    await message.answer(f'Чтобы поменять данные вечер, нажмите кнопку!', reply_markup=start_close)
    await state.reset_state(with_data=False)

def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_message_handler(add_user_name, state=Name.send_name)
    dp.register_message_handler(user_save, commands=["save"])
    dp.register_message_handler(user_edit_back, commands=["edit"])
