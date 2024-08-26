# init_db.py

import sqlite3

conn = sqlite3.connect("./data/database.db")
curs = conn.cursor()

curs.execute("DROP TABLE IF EXISTS users;")
curs.execute(
    """
        CREATE TABLE IF NOT EXISTS users
        (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
        );
    """
)

curs.execute("DROP TABLE IF EXISTS parties;")
curs.execute(
    """
                CREATE TABLE IF NOT EXISTS parties
                (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                date TEXT NOT NULL,
                venue TEXT NOT NULL,
                main_dish TEXT NOT NULL,
                attendees INTEGER NOT NULL,
                created TEXT DEFAULT CURRENT_TIMESTAMP
                );
             """
)

conn.commit()
conn.close()
