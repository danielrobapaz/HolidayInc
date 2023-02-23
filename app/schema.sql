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

CREATE TABLE user_proyect (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER NOT NULL,
    proyectid INTEGER NOT NULL,
    FOREIGN KEY (userid) references user(id),
    FOREIGN KEY (proyectid) references proyect(id)
);

CREATE TABLE logger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eventid INTEGER NOT NULL,
    date TEXT NOT NULL,
    user TEXT NOT NULL,
    system TEXT NOT NULL,
    log_text TEXT NOT NULL,
    FOREIGN KEY (user) references user(username),
    -- FOREIGN KEY (system) references systems(id),
    -- FOREIGN KEY (eventid) references events(id)
);

CREATE TABLE systems {
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NO NULL
}

CREATE TABLE events {
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    system TEXT NOT NULL,
    FOREIGN KEY (system) REFERENCES systems(id)
}

CREATE TABLE proyect (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT UNIQUE NOT NULL,
    start DATE NOT NULL,
    end DATE NOT NULL,
    status INTEGER
);