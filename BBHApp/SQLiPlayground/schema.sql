-- Drop old tables
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS flags;
DROP TABLE IF EXISTS submissions;
DROP TABLE IF EXISTS challenges;
DROP TABLE IF EXISTS feedback;

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

-- Feedback (with moderation)
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comment TEXT,
    status TEXT DEFAULT 'pending',
    approved INTEGER DEFAULT 0,
    moderated_by TEXT
);

-- Preload users
INSERT INTO users (username, password, email, role) VALUES
('admin', 'admin123', 'admin@example.com', 'admin'),
('guest', 'guest', 'guest@example.com', 'user'),
('jdoe', 'password', 'jdoe@example.com', 'user');

-- Preload flags
INSERT INTO flags (challenge_name, flag_value) VALUES
('Classic SQLi', 'FLAG{classic_sqli_exploited}'),
('Union SQLi', 'FLAG{union_sqli_extracted}'),
('Stacked SQLi', 'FLAG{stacked_query_executed}'),
('Session Hijack', 'FLAG{session_hijack}'),
('Admin Panel Access', 'FLAG{admin_area_access}'),
('Reflected XSS', 'FLAG{xss_reflected}'),
('Stored XSS', 'FLAG{xss_stored}'),
('DOM XSS', 'FLAG{xss_dom}'),
('JWT Tampering', 'FLAG{jwt_token_tampering}'),
('JWT None Algorithm', 'FLAG{jwt_none_alg_bypass}'),
('JWT Key Confusion', 'FLAG{jwt_key_confusion_rs256_to_hs256}'),
('Recon - robots.txt', 'FLAG{disallowed_path_discovered}'),
('Recon - .env', 'FLAG{env_file_exposed}'),
('Recon - git config', 'FLAG{git_config_leaked}'),
('Recon - DS_Store', 'FLAG{ds_store_index_revealed}'),
('Recon - Hidden Admin Panel', 'FLAG{found_hidden_admin_panel}'),
('Exposed Backup File', 'FLAG{backup_archive_exposed}'),
('Shell Trigger', 'FLAG{lfi_shell_triggered}'),
('LFI Reverse Shell', 'FLAG{reverse_shell_triggered}');

-- Preload challenges
INSERT INTO challenges (name, description, difficulty, flag_value, hint) VALUES
('Classic SQLi', 'Use basic SQL injection to dump user data.', 'Easy', 'FLAG{classic_sqli_exploited}', "Try injecting ' OR 1=1--"),
('Union SQLi', 'Use UNION SELECT to extract extra data.', 'Medium', 'FLAG{union_sqli_extracted}', "Try UNION SELECT 1, 'admin'--"),
('Stacked SQLi', 'Use stacked queries to escalate privileges.', 'Hard', 'FLAG{stacked_query_executed}', "Try stacked SELECT and UPDATE."),
('Session Hijack', 'Leak session IDs to hijack user access.', 'Medium', 'FLAG{session_hijack}', "Try enumerating common usernames."),
('Admin Panel Access', 'Escalate access to admin dashboard.', 'Hard', 'FLAG{admin_area_access}', "Try setting a cookie or role manually."),
('Reflected XSS', 'Inject JavaScript via GET parameter.', 'Easy', 'FLAG{xss_reflected}', 'Try ?msg=<script>alert(1)</script>'),
('Stored XSS', 'Store and trigger XSS via form.', 'Medium', 'FLAG{xss_stored}', 'Try submitting a <script> tag.'),
('DOM XSS', 'Manipulate JS DOM to trigger XSS.', 'Medium', 'FLAG{xss_dom}', 'Use URL fragment to inject code.'),
('JWT Tampering', 'Tamper with HS256-signed JWT tokens.', 'Medium', 'FLAG{jwt_token_tampering}', 'Use jwt.io to modify the token.'),
('JWT None Algorithm', 'Abuse JWT alg "none".', 'Hard', 'FLAG{jwt_none_alg_bypass}', 'Create a JWT with "alg": "none".'),
('JWT Key Confusion', 'Exploit RS256 to HS256 confusion.', 'Hard', 'FLAG{jwt_key_confusion_rs256_to_hs256}', 'Sign RS256 token with public key.'),
('Recon - robots.txt', 'Check for disallowed paths.', 'Easy', 'FLAG{disallowed_path_discovered}', 'Visit /robots.txt'),
('Recon - .env', 'Discover secrets in .env.', 'Medium', 'FLAG{env_file_exposed}', 'Try accessing /.env'),
('Recon - git config', 'Leak Git repository config.', 'Medium', 'FLAG{git_config_leaked}', 'Try accessing /.git/config'),
('Recon - DS_Store', 'Extract file structure via .DS_Store.', 'Medium', 'FLAG{ds_store_index_revealed}', 'Access /.DS_Store'),
('Recon - Hidden Admin Panel', 'Discover hidden admin page.', 'Medium', 'FLAG{found_hidden_admin_panel}', 'Enumerate /secret_dashboard'),
('Exposed Backup File', 'Analyze leaked zip contents.', 'Medium', 'FLAG{backup_archive_exposed}', 'Try /backup.zip'),
('Shell Trigger', 'Include shell.php to simulate shell execution.', 'Hard', 'FLAG{lfi_shell_triggered}', 'Try including shell.php via ?page='),
('LFI Reverse Shell', 'Run a simulated shell command and extract flag.', 'Hard', 'FLAG{reverse_shell_triggered}', 'Try /shell?cmd=id');
