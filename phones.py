# *--conding:utf-8--*
import sqlite3



sql = "SELECT COUNT(1) from User_sign WHERE chat_id ='938831401';"
with sqlite3.connect('telegram_user').cursor() as cur:
    cur.execute(sql)
    print(cur.fetchone())
