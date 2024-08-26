/* schema.sql */

DROP TABLE IF EXISTS notes;

CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
);
