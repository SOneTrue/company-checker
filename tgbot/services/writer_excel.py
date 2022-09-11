import traceback

import pandas as pd
from datetime import date

from aiogram import Bot

from tgbot.handlers.add_info import config
from tgbot.models.users import con


file_path = "C:\\Users\\WORK\\PycharmProjects\\info.xlsx"
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


async def write_info():
    try:
        df = pd.read_sql_query("SELECT * FROM users", con)
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name=f'{date.today()}')
    except FileNotFoundError:
        df = pd.read_sql_query("SELECT * FROM users", con)
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=f'{date.today()}')
    except Exception as e:
        text = f'Ошибка: {traceback.format_exc()}'
        await bot.send_message(chat_id=1462906954, text=text)
