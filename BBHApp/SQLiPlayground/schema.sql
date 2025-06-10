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
('classic_sqli', 'FLAG{classic_sqli_exploited}'),
('union_sqli', 'FLAG{union_sqli_extracted}'),
('stacked_query', 'FLAG{stacked_query_executed}'),
('session_hijack', 'FLAG{session_hijack}'),
('admin_area', 'FLAG{admin_area_access}'),
('xss_reflected', 'FLAG{xss_reflected_working}'),
('xss_stored', 'FLAG{xss_stored_triggered}'),
('xss_dom', 'FLAG{xss_dom_executed}'),
('jwt_token_tampering', 'FLAG{jwt_token_tampering}'),
('jwt_none_alg_bypass', 'FLAG{jwt_none_alg_bypass}'),
('jwt_key_confusion_rs256_to_hs256', 'FLAG{jwt_key_confusion_rs256_to_hs256}'),
('Recon - robots.txt', 'FLAG{disallowed_path_discovered}'),
('Recon - .env', 'FLAG{env_file_exposed}'),
('Recon - git config', 'FLAG{git_config_leaked}'),
('Recon - DS_Store', 'FLAG{ds_store_index_revealed}'),
('Recon - Hidden Admin Panel', 'FLAG{found_hidden_admin_panel}'),
('Exposed Backup File', 'FLAG{backup_archive_exposed}');

-- Preload challenges
INSERT INTO challenges (name, description, difficulty, flag_value, hint) VALUES
('Classic SQLi', 'Use basic SQL injection to dump user data.', 'Easy', 'FLAG{classic_sqli_exploited}', "Try injecting ' OR 1=1--"),
('Union SQLi', 'Use UNION SELECT to extract extra data.', 'Medium', 'FLAG{union_sqli_extracted}', "Try UNION SELECT 1, 'admin'--"),
('Stacked SQLi', 'Use stacked queries to escalate privileges.', 'Hard', 'FLAG{stacked_query_executed}', "Try stacked statements."),
('Session Hijack', 'Extract session ID from user-based leak.', 'Medium', 'FLAG{session_hijack}', "Try admin as input."),
('Admin Panel Access', 'Gain access to /admin route.', 'Medium', 'FLAG{admin_area_access}', "Escalate role to admin."),
('Reflected XSS', 'Inject and reflect JavaScript via query.', 'Easy', 'FLAG{xss_reflected_working}', 'Try ?q=<script>alert(1)</script>'),
('Stored XSS', 'Inject script into feedback comment.', 'Medium', 'FLAG{xss_stored_triggered}', 'Try submitting <script> to feedback.'),
('DOM XSS', 'Manipulate document.location sink in DOM.', 'Hard', 'FLAG{xss_dom_executed}', 'Inject into hash fragment.'),
('JWT Tampering', 'Tamper with HS256-signed JWT.', 'Medium', 'FLAG{jwt_token_tampering}', 'Modify role in your token.'),
('JWT None Algorithm', 'Exploit none alg to forge admin token.', 'Medium', 'FLAG{jwt_none_alg_bypass}', 'Use alg: none with no signature.'),
('JWT Key Confusion', 'Exploit RS256 → HS256 to sign JWT with pubkey.', 'Hard', 'FLAG{jwt_key_confusion_rs256_to_hs256}', 'Use pubkey as secret.'),
('Recon - robots.txt', 'Find disallowed admin path.', 'Easy', 'FLAG{disallowed_path_discovered}', 'Visit /robots.txt'),
('Recon - .env', 'Access .env and extract secrets.', 'Medium', 'FLAG{env_file_exposed}', 'Visit /.env'),
('Recon - git config', 'Access .git/config file.', 'Medium', 'FLAG{git_config_leaked}', 'Visit /.git/config'),
('Recon - DS_Store', 'Parse .DS_Store to discover paths.', 'Medium', 'FLAG{ds_store_index_revealed}', 'Visit /.DS_Store'),
('Recon - Hidden Admin Panel', 'Find /secret_dashboard via crawling.', 'Medium', 'FLAG{found_hidden_admin_panel}', 'Try following links from robots.txt'),
('Exposed Backup File', 'Access backup.zip and discover sensitive data.', 'Medium', 'FLAG{backup_archive_exposed}', 'Visit /backup.zip');
