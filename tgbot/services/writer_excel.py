import pandas as pd
from datetime import date

from tgbot.models.users import con

writer = pd.ExcelWriter('../info.xlsx', engine='xlsxwriter')
current_date = date.today()

def write_info():
    df = pd.read_sql_query("SELECT * FROM users", con)
    print(df)
    df.to_excel(writer, sheet_name=f'{current_date}')
    writer.save()
