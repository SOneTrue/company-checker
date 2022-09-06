import pandas as pd
from datetime import date

from aiogram import Bot

from tgbot.handlers.add_info import config
from tgbot.models.users import con

path = '../info.xlsx'
new_date = date.today()
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


async def write_info():
    try:
        df = pd.read_sql_query("SELECT * FROM users", con)
        with pd.ExcelWriter(path, engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name=f'{new_date}')
    except FileNotFoundError:
        df = pd.read_sql_query("SELECT * FROM users", con)
        with pd.ExcelWriter(path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=f'{new_date}')
    except ValueError:
        text = 'Возникла ошибка записи информации в таблицу!'
        await bot.send_message(chat_id=1462906954, text=text)
