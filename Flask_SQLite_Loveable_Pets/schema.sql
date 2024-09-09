/* schema.sql */

DROP TABLE IF EXISTS pets;

CREATE TABLE IF NOT EXISTS pets
(
    id INTEGER PRIMARY KEY,
    type VARCHAR(30) NOT NULL,
    name VARCHAR(50) NOT NULL,
    age INTEGER NOT NULL,
    description TEXT NOT NULL,
    url TEXT NOT NULL
);
