DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS logger;
DROP TABLE IF EXISTS proyect;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS proyectStatus;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS cars;
DROP TABLE IF EXISTS carBrands;
DROP TABLE IF EXISTS carModels;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS problems;
DROP TABLE IF EXISTS proyectClients;
DROP TABLE IF EXISTS metricsUnit;
DROp TABLE IF EXISTS actionPlan;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    firstname TEXT NOT NULL,
    secondname TEXT NOT NULL,
    password TEXT NOT NULL,
    roleId INTEGER,
    proyId INTEGER,
    auth INTEGER,

    FOREIGN KEY (roleId) REFERENCES roles(id),
    FOREIGN KEY (proyId) REFERENCES proyect(id)
);

CREATE TABLE proyect (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT UNIQUE NOT NULL,
    start DATE NOT NULL,
    end DATE NOT NULL,
    statusId INTEGER,

    FOREIGN KEY (statusId) REFERENCES proyectStatus(id)
);

CREATE TABLE logger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT NOT NULL,
    date TEXT NOT NULL,
    user TEXT NOT NULL
);

CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE proyectStatus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dni TEXT NOT NULL UNIQUE,
    firstname TEXT NOT NULL,
    secondname TEXT NOT NULL,
    birthday TEXT NOT NULL,
    tlf TEXT NOT NULL,
    mail TEXT NOT NULL,
    address TEXT NOT NULL
);

CREATE TABLE cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ownerId INTEGER NOT NULL,
    plaque TEXT NOT NULL,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    bodyWorkSerial TEXT NOT NULL,
    motorSerial TEXT NOT NULL,
    color TEXT NOT NULL,
    problem TEXT NOT NULL,

    FOREIGN KEY (ownerId) REFERENCES clients(id)
);

CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL UNIQUE
);

CREATE TABLE problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem TEXT NOT NULL UNIQUE,
    depId INTEGER NOT NULL,

    FOREIGN KEY (depId) REFERENCES departments(id)
);

CREATE TABLE proyectClients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proyId INTEGER NOT NULL,
    clientId INTEGER NOT NULL,
    carId INTEGER NOT NULL,
    managerId INTEGER NOT NULL,
    departmentId INTEGER NOT NULL,
    problemId INTEGER NOT NULL,
    solution TEXT NOT NULL,
    subtotal INTEGER DEFAULT 0,
    observation TEXT,

    FOREIGN KEY (proyId) REFERENCES proyect(id),
    FOREIGN KEY (clientId) REFERENCES clients(id),
    FOREIGN KEY (carId) REFERENCES cars(id),
    FOREIGN KEY (managerId) REFERENCES user(id),
    FOREIGN KEY (departmentId) REFERENCES departments(id),
    FOREIGN KEY (problemId) REFERENCES problems(id)
);

CREATE TABLE metricsUnit (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  dimension INTEGER NOT NULL,
  unit TEXT NOT NULL  
);

CREATE TABLE actionPlan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proyectClientId INTEGER NOT NULL,
    action TEXT NOT NULL,
    activity TEXT NOT NULL,
    start DATE NOT NULL,
    end DATE NOT NULL,
    hours INTEGER NOT NULL,
    responsibleId INTEGER NOT NULL,
    nWorkers INTEGER NOT NULL,
    costPerHour INTEGER NOT NULL,
    totalHumanTalent INTEGER NOT NULL,
    category INTEGER,
    supplieName TEXT,
    metricId INTEGER,
    costSupplie INTEGER,
    totalSupplie INTEGET DEFAULT 0,
    total INTEGER NOT NULL,

    FOREIGN KEY (proyectClientId) REFERENCES proyectClients(id),
    FOREIGN KEY (responsibleId) REFERENCES user(id),
    FOREIGN KEY (metricId) REFERENCES metricsUnit(id)
);