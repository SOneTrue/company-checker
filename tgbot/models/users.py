import sqlite3
from sqlite3 import IntegrityError

con = sqlite3.connect("tgbot/models/database.db")
cur = con.cursor()


async def add_user(telegram_id, username, fname, lname, real_name, number_auto, road_list, odometer, odometer_back,
                   litre_back):
    sql = """INSERT INTO users("Телеграм ID", "Пользовательский ник", "Имя", "Фамилия", "Полное имя", "Номер авто", 
    "Путевой лист", "Одометр выезд", "Одометр заезд", "Литров заезд")
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    data = (telegram_id, username, fname, lname, real_name, number_auto, road_list, odometer, odometer_back, litre_back)
    try:
        cur.execute(sql, data)
        con.commit()
    except IntegrityError:
        con.commit()
        pass


async def update_user(telegram_id, rname):
    sql = """Update users set "Полное имя" = ? where "Телеграм ID" = ?"""
    data = (rname, telegram_id)
    cur.execute(sql, data)
    con.commit()

async def update_info_user(telegram_id, real_name, number_auto, road_list, odometer, odometer_back, litre_back):
    sql = """Update users set "Полное имя" = ?, "Номер авто" = ?, "Путевой лист" = ?, "Одометр выезд" = ?, "Одометр заезд" = ?, 
    "Литров заезд" = ? where "Телеграм ID" = ?"""
    data = (real_name, number_auto, road_list, odometer, odometer_back, litre_back, telegram_id)
    cur.execute(sql, data)
    con.commit()


async def delete_info():
    sql = """DELETE FROM users"""
    cur.execute(sql)
    con.commit()

