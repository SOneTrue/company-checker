import pandas as pd
from datetime import date

from tgbot.models.users import con

path = '../info.xlsx'
new_date = date.today()


async def write_info():
    try:
        df = pd.read_sql_query("SELECT * FROM users", con)
        with pd.ExcelWriter(path, engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name=f'{new_date}')
    except FileNotFoundError:
        df = pd.read_sql_query("SELECT * FROM users", con)
        with pd.ExcelWriter(path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=f'{new_date}')
