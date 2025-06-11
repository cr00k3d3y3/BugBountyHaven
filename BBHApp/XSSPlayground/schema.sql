-- schema.sql for XSSPlayground

DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS submissions;
DROP TABLE IF EXISTS flags;

CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint TEXT,
    ip TEXT,
    payload TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    flag_value TEXT,
    challenge_name TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE flags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    challenge_name TEXT,
    flag_value TEXT
);

INSERT INTO flags (challenge_name, flag_value) VALUES 
('Reflected XSS', 'FLAG{reflected_xss_triggered}'),
('Stored XSS', 'FLAG{stored_xss_executed}'),
('DOM XSS', 'FLAG{dom_xss_triggered}');
