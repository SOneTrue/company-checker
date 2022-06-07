import sqlite3

con = sqlite3.connect("tgbot/models/database.db")
cur = con.cursor()


async def add_user(telegram_id, username, fname, lname, rname, number_auto, road_list, odometer, odometer_back,
                   litre_back):
    sql = """INSERT INTO users(telegram_id, username, fname, lname, rname, number_auto, road_list, odometer, 
    odometer_back, litre_back)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    data = (telegram_id, username, fname, lname, rname, number_auto, road_list, odometer, odometer_back, litre_back)
    cur.execute(sql, data)
    con.commit()


async def get_user():
    sql = """SELECT * from users"""
    cur.execute(sql)
    row = cur.fetchall()
    return row


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
