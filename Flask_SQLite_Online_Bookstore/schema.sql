/* schema.sql */

DROP TABLE IF EXISTS books;

CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    author TEXT NOT NULL,
    count TEXT NOT NULL,
    created TEXT DEFAULT CURRENT_TIMESTAMP 
);
