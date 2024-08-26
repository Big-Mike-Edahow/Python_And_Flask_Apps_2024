# init_db.py

import sqlite3

conn = sqlite3.connect("./data/database.db")
curs = conn.cursor()

curs.execute("DROP TABLE IF EXISTS travelers;")
curs.execute(
    """
        CREATE TABLE IF NOT EXISTS travelers
        (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
        );
    """
)

curs.execute("DROP TABLE IF EXISTS posts;")
curs.execute(
    """
                CREATE TABLE IF NOT EXISTS posts
                (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                city TEXT NOT NULL,
                country TEXT NOT NULL,
                description TEXT NOT NULL,
                created TEXT DEFAULT CURRENT_TIMESTAMP
                );
             """
)

conn.commit()
conn.close()
