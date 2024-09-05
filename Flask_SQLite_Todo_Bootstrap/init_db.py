# init_db.py

import sqlite3

conn = sqlite3.connect("./data/database.db")

with open("schema.sql") as f:
    conn.executescript(f.read())

curs = conn.cursor()

curs.execute(
    "INSERT INTO posts (title, content) VALUES (?, ?)",
    ("First Post", "Content for the first post"),
)

curs.execute(
    "INSERT INTO posts (title, content) VALUES (?, ?)",
    ("Second Post", "Content for the second post"),
)

conn.commit()
conn.close()
