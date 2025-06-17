DROP TABLE IF EXISTS system_users;
CREATE TABLE system_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_login TEXT
);

DROP TABLE IF EXISTS visitors;
CREATE TABLE visitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    id_number TEXT NOT NULL,
    phone TEXT NOT NULL,
    purpose TEXT NOT NULL,
    visit_time TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL
);