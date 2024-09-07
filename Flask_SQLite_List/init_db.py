# init_db.py

import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__))

conn = sqlite3.connect(basedir + "/data/database.db")

with open("schema.sql") as f:
    conn.executescript(f.read())

curs = conn.cursor()

conn.commit()
conn.close()
