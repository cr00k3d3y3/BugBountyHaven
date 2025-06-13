CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user'
);

CREATE TABLE IF NOT EXISTS flags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    challenge_name TEXT,
    flag_value TEXT
);

CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    flag_value TEXT,
    challenge_name TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint TEXT,
    ip TEXT,
    payload TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO flags (challenge_name, flag_value) VALUES
('GraphQL Introspection Exposure', 'FLAG{graphql_introspection_exposed}'),
('Nested Query DoS', 'FLAG{graphql_nested_query_dos}'),
('GraphQL Auth Bypass', 'FLAG{graphql_auth_bypass}');

INSERT INTO users (username, password, email, role) VALUES
('admin', 'adminpass', 'admin@example.com', 'admin'),
('guest', 'guestpass', 'guest@example.com', 'user'),
('alice', 'alicealice', 'alice@example.com', 'user'),
('bob', 'bobbob', 'bob@example.com', 'user'),
('charlie', 'charliebrown', 'charlie@example.com', 'user');
