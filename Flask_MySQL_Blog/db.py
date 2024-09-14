# db.py

import pymysql

def getDB():
    conn = pymysql.connect(
        host="localhost",
        user="mike",
        password="5454160s",
        database="my_db"
    )
    return conn
