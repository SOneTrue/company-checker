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


async def update_user(rname, telegram_id):
    sql = """Update users set rname = ? where telegram_id = ?"""
    data = (rname, telegram_id)
    cur.execute(sql, data)
    con.commit()
    print(f'Запись {data}, обновлена')
