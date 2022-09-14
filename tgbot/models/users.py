import sqlite3
from sqlite3 import IntegrityError

from aiogram import Bot

from tgbot.handlers.add_info import config

bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

file_path = "C:\\Users\\WORK\\PycharmProjects\\company-checker\\tgbot\\models\\database.db"
con = sqlite3.connect(file_path)
cur = con.cursor()


async def add_user(telegram_id, username, real_name, number_auto, road_list, odometer, odometer_back, litre_back):
    sql = """INSERT INTO users("Телеграм ID", "Пользовательский ник", "Полное имя", "Номер авто", "Путевой лист", 
    "Одометр выезд", "Одометр заезд", "Литров заезд")
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
    data = (telegram_id, username, real_name, number_auto, road_list, odometer, odometer_back, litre_back)
    try:
        cur.execute(sql, data)
        con.commit()
    except IntegrityError:
        sql = """Update users set "Полное имя" = ? where "Телеграм ID" = ?"""
        data = (real_name, telegram_id)
        cur.execute(sql, data)
        con.commit()


async def update_user(telegram_id, real_name):
    sql = """Update users set "Полное имя" = ? where "Телеграм ID" = ?"""
    data = (real_name, telegram_id)
    cur.execute(sql, data)
    con.commit()


async def update_info_user(real_name, number_auto, road_list, odometer, odometer_back, litre_back, telegram_id):
    sql = """Update users set "Полное имя" = ?, "Номер авто" = ?, "Путевой лист" = ?, "Одометр выезд" = ?, 
    "Одометр заезд" = ?, "Литров заезд" = ? where "Телеграм ID" = ?"""
    data = (real_name, number_auto, road_list, odometer, odometer_back, litre_back, telegram_id)
    cur.execute(sql, data)
    con.commit()


async def delete_info():
    sql = """DELETE FROM users"""
    cur.execute(sql)
    con.commit()