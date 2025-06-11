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
('Exposed Backup File', 'FLAG{backup_archive_exposed}'),
('Shell Trigger', 'FLAG{lfi_shell_triggered}'),
('LFI Reverse Shell', 'FLAG{reverse_shell_triggered}');

-- Preload challenges
INSERT INTO challenges (name, description, difficulty, flag_value, hint) VALUES
('Exposed Backup File', 'Analyze leaked zip contents.', 'Medium', 'FLAG{backup_archive_exposed}', 'Try /backup.zip'),
('Shell Trigger', 'Include shell.php to simulate shell execution.', 'Hard', 'FLAG{lfi_shell_triggered}', 'Try including shell.php via ?page='),
('LFI Reverse Shell', 'Run a simulated shell command and extract flag.', 'Hard', 'FLAG{reverse_shell_triggered}', 'Try /shell?cmd=id');
