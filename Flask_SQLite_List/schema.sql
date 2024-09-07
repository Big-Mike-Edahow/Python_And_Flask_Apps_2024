/* schema.sql */

DROP TABLE IF EXISTS entries;

CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    status INTEGER DEFAULT 0,
    created TEXT DEFAULT CURRENT_TIMESTAMP
);
