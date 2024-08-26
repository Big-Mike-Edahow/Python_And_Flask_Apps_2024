# init_db.py

import sqlite3

conn = sqlite3.connect('database.db')
curs = conn.cursor()

with open('schema.sql') as f:
    conn.executescript(f.read())

curs.execute('''INSERT INTO todos (todo) VALUES ("Study Python and Flask")''')
curs.execute('''INSERT INTO todos (todo) VALUES ("Drive to Guntersville, AL")''')

conn.commit()
conn.close()
