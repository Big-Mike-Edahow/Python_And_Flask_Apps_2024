# init_db.py

import sqlite3

conn = sqlite3.connect("./data/database.db")

with open("schema.sql") as f:
    conn.executescript(f.read())

curs = conn.cursor()

curs.execute('''INSERT INTO todos(todo) VALUES("Eat lunch at McDonald's in Rexburg.");''')
curs.execute('''INSERT INTO todos(todo) VALUES("Study web development at the library.");''')

conn.commit()
conn.close()
