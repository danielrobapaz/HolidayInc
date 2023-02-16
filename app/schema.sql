DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS proyect;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    firstname TEXT NOT NULL,
    secondname TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT,
    proyId INTEGER,
    auth INTEGER
);

CREATE TABLE proyect (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT UNIQUE NOT NULL,
    start DATE NOT NULL,
    end DATE NOT NULL,
    status INTEGER
);