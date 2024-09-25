# db.py

import pymysql

def getDB():
    conn = pymysql.connect(
        host="localhost",
        user="foo",
        password="bar",
        database="my_db"
    )
    return conn
