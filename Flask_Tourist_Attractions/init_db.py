# init_db.py

import sqlite3

conn = sqlite3.connect("./data/database.db")
curs = conn.cursor()

curs.execute("DROP TABLE IF EXISTS attractions;")
curs.execute(
    """
        CREATE TABLE IF NOT EXISTS attractions
        (
        id INTEGER PRIMARY KEY,
        attraction TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL,
        image_url TEXT NOT NULL,
        created TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """
)

conn.commit()
conn.close()
