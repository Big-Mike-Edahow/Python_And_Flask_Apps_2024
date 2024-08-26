# init_db.py

import sqlite3

conn = sqlite3.connect("./data/database.db")
curs = conn.cursor()

curs.execute("DROP TABLE IF EXISTS confessions;")
curs.execute(
    """
        CREATE TABLE IF NOT EXISTS confessions
        (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        confession TEXT NOT NULL,
        created TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """
)

conn.commit()
conn.close()
