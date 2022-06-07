import sqlite3
from sqlite3 import IntegrityError

con = sqlite3.connect("tgbot/models/database.db")
cur = con.cursor()


async def add_user(telegram_id, username, fname, lname, rname, number_auto, road_list, odometer, odometer_back,
                   litre_back):
    sql = """INSERT INTO users(telegram_id, username, fname, lname, rname, number_auto, road_list, odometer, 
    odometer_back, litre_back)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    data = (telegram_id, username, fname, lname, rname, number_auto, road_list, odometer, odometer_back, litre_back)
    try:
        cur.execute(sql, data)
        con.commit()
    except IntegrityError:
        pass

# async def get_user(telegram_id):
#     sql = """SELECT * from users where telegram_id = ?"""
#     cur.execute(sql, (telegram_id,))
#     row = cur.fetchone()
#     con.commit()
#     if row:
#         return True
#     else:
#         return False


async def update_user(telegram_id, rname):
    sql = """Update users set rname = ? where telegram_id = ?"""
    data = (rname, telegram_id)
    cur.execute(sql, data)
    con.commit()


async def rname_user(telegram_id):
    sql = """select rname from users where telegram_id = ?"""
    cur.execute(sql, (telegram_id,))
    params = cur.fetchone()
    return params


async def update_info_user(telegram_id, number_auto, road_list, odometer, odometer_back, litre_back):
    sql = """Update users set number_auto = ?, road_list = ?, odometer = ?, odometer_back = ?, litre_back = ? where telegram_id = ?"""
    data = (number_auto, road_list, odometer, odometer_back, litre_back, telegram_id)
    cur.execute(sql, data)
    con.commit()
