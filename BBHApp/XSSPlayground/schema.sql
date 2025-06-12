-- Drop old tables
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS flags;
DROP TABLE IF EXISTS submissions;
DROP TABLE IF EXISTS challenges;


-- Users
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    email TEXT,
    role TEXT DEFAULT 'user'
);

-- Logs
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint TEXT,
    ip TEXT,
    payload TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Flags
CREATE TABLE flags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    challenge_name TEXT,
    flag_value TEXT
);

-- Submissions
CREATE TABLE submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    flag_value TEXT,
    challenge_name TEXT,
    stars INTEGER DEFAULT 1,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Challenges
CREATE TABLE challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    difficulty TEXT,
    flag_value TEXT,
    hint TEXT
);


-- Preload users
INSERT INTO users (username, password, email, role) VALUES
('admin', 'admin123', 'admin@example.com', 'admin'),
('guest', 'guest', 'guest@example.com', 'user'),
('jdoe', 'password', 'jdoe@example.com', 'user');

-- Preload flags
INSERT INTO flags (challenge_name, flag_value) VALUES
('Reflected XSS', 'FLAG{xss_reflected_working}'),
('Stored XSS', 'FLAG{xss_stored_triggered}'),
('DOM XSS', 'FLAG{dom_xss_triggered}');


-- Preload challenges
INSERT INTO challenges (name, description, difficulty, flag_value, hint) VALUES
('Reflected XSS', 'Inject JavaScript via GET parameter.', 'Easy', 'FLAG{xss_reflected_working}', 'Try ?msg=<script>alert(1)</script>'),
('Stored XSS', 'Store and trigger XSS via form.', 'Medium', 'FLAG{xss_stored_triggered}', 'Try submitting a <script> tag.'),
('DOM XSS', 'Manipulate JS DOM to trigger XSS.', 'Medium', 'FLAG{dom_xss_triggered}', 'Use URL fragment to inject code.');


