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
