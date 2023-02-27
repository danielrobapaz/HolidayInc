DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS logger;
DROP TABLE IF EXISTS systems;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS proyect;
DROP TABLE IF EXISTS user_proyect;
DROP TABLE IF EXISTS roles;

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

CREATE TABLE logger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT NOT NULL,
    date TEXT NOT NULL,
    user TEXT NOT NULL
);

CREATE TABLE systems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NO NULL
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    system TEXT NOT NULL,
    FOREIGN KEY (system) REFERENCES systems(id)
);

CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL
);

CREATE TABLE proyect (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT UNIQUE NOT NULL,
    start DATE NOT NULL,
    end DATE NOT NULL,
    status INTEGER
);

CREATE TABLE user_proyect (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER NOT NULL,
    proyectid INTEGER NOT NULL,
    FOREIGN KEY (userid) references user(id),
    FOREIGN KEY (proyectid) references proyect(id)
);