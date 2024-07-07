# init_db.py

import sqlite3

conn = sqlite3.connect("database.db")


with open("schema.sql") as f:
    conn.executescript(f.read())

curs = conn.cursor()

curs.execute("INSERT INTO notes (content) VALUES (?)", ("Study Python and Flask.",))
curs.execute("INSERT INTO notes (content) VALUES (?)", ("Get a good night's sleep.",))
curs.execute("INSERT INTO notes (content) VALUES (?)", ("Make delivery in Denver in the morning.",),)

conn.commit()
conn.close()
