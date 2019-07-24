# *--conding:utf-8--*
import sqlite3


def creat_table():
    """创建表"""
    conncet = sqlite3.connect('telegram_user')
    curs = conncet.cursor()
    curs.execute(
        "create table User_sign(id integer PRIMARY KEY AUTOINCREMENT,user_name varchar(255),chat_id int(11),is_sign int (1) default 1,time TIMESTAMP default (datetime('now','localtime')))")

    curs.close()
    conncet.close()
