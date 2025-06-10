-- schema.sql for SQLiPlayground
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS flags;
DROP TABLE IF EXISTS submissions;
DROP TABLE IF EXISTS challenges;
DROP TABLE IF EXISTS feedback;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    email TEXT,
    role TEXT DEFAULT 'user'
);

CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint TEXT,
    ip TEXT,
    payload TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE flags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    challenge_name TEXT,
    flag_value TEXT
);

CREATE TABLE submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    flag_value TEXT,
    challenge_name TEXT,
    stars INTEGER DEFAULT 1,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    difficulty TEXT,
    flag_value TEXT,
    hint TEXT
);

CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comment TEXT,
    status TEXT DEFAULT 'pending',
    flagged INTEGER DEFAULT 0,
    approved INTEGER DEFAULT 0
);

INSERT INTO users (username, password, email, role) VALUES
('admin', 'admin123', 'admin@example.com', 'admin'),
('guest', 'guest', 'guest@example.com', 'user'),
('jdoe', 'password', 'jdoe@example.com', 'user');

INSERT INTO flags (challenge_name, flag_value) VALUES
('classic_sqli', 'FLAG{classic_sqli_exploited}'),
('union_sqli', 'FLAG{union_sqli_extracted}'),
('stacked_query', 'FLAG{stacked_query_executed}'),
('session_hijack', 'FLAG{session_hijack}'),
('admin_area', 'FLAG{admin_area_access}'),
('Recon - robots.txt', 'FLAG{disallowed_path_discovered}'),
('Recon - .env', 'FLAG{env_file_exposed}'),
('Recon - git config', 'FLAG{git_config_leaked}'),
('Recon - DS_Store', 'FLAG{ds_store_index_revealed}'),
('Recon - Admin Panel', 'FLAG{admin_interface_exposed}');

INSERT INTO challenges (name, description, difficulty, flag_value, hint) VALUES
('Classic SQLi', 'Use basic SQL injection to dump user data.', 'Easy', 'FLAG{classic_sqli_exploited}', "Try injecting ' OR 1=1--"),
('Union SQLi', 'Use UNION SELECT to extract extra data.', 'Medium', 'FLAG{union_sqli_extracted}', "Try UNION SELECT 1, 'admin'--"),
('Stacked SQLi', 'Use stacked queries to escalate privileges.', 'Hard', 'FLAG{stacked_query_executed}', "Try: SELECT 1; UPDATE users SET role='admin' WHERE username='guest';"),
('Session Hijack', 'Extract session identifier from leakage.', 'Medium', 'FLAG{session_hijack}', 'Try common usernames to trigger fake leaks.'),
('Admin Panel Access', 'Use any exploit to access /admin.', 'Medium', 'FLAG{admin_area_access}', 'Try escalating role to admin.'),
('Recon - robots.txt', 'Discover hidden paths in robots.txt.', 'Easy', 'FLAG{disallowed_path_discovered}', 'Visit /robots.txt and follow the path.'),
('Recon - .env', 'Check for sensitive environment config exposure.', 'Medium', 'FLAG{env_file_exposed}', 'Try accessing /.env'),
('Recon - git config', 'Find and read exposed .git/config file.', 'Medium', 'FLAG{git_config_leaked}', 'Access /.git/config'),
('Recon - DS_Store', 'Parse .DS_Store to reveal file paths.', 'Medium', 'FLAG{ds_store_index_revealed}', 'Access /.DS_Store and observe output.'),
('Recon - Admin Panel', 'Access an exposed admin interface.', 'Medium', 'FLAG{admin_interface_exposed}', 'Try accessing /admin-panel directly.');
