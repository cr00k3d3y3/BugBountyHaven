---

## 🔍 Challenge Overview: UNION-Based SQL Injection

**Type:** SQL Injection (UNION-Based)
**Difficulty:** Beginner → Intermediate
**Goal:** Extract information from the database using UNION-based SQL injection.

---

### 🧠 What Is UNION-Based SQL Injection?

UNION-based SQLi is a subtype of classic SQL injection where an attacker leverages the `UNION` SQL operator to combine the results of two or more SELECT statements. When the application fails to properly sanitize user input, it becomes possible to append a malicious `UNION SELECT` statement to extract data from other tables in the database.

This method is particularly dangerous when verbose SQL error messages or debug info is exposed.

**Use Cases:**

* Enumerating database structure
* Dumping user credentials or PII
* Bypassing filters via crafted payloads

---

### 🧬 How It Works (Step-by-Step)

#### 1. **Client Request**

The user inputs something like:

```
admin' UNION SELECT 1, 'other_user'--
```

#### 2. **Server-Side Query Construction**

If the app concatenates input like so:

```sql
SELECT id, username FROM users WHERE username = '<input>'
```

It becomes:

```sql
SELECT id, username FROM users WHERE username = 'admin' UNION SELECT 1, 'other_user'--'
```

#### 3. **Server Response**

* If the number and type of columns match, it executes.
* The app might show `other_user` on the frontend, indicating success.

---

### 🧪 Common Missteps (Bad Payloads)

#### ❌ Wrong number of columns

```sql
' UNION SELECT 1--
```

**Why it fails:** The original query selects two columns, but the payload only returns one.

#### ❌ Wrong data types

```sql
' UNION SELECT 'abc', 123--
```

**Why it fails:** Data types must match (e.g., `username` likely expects TEXT).

#### ❌ Syntax errors

```sql
' UNION SELECT * FROM users--
```

**Why it fails:** Using `*` can mismatch the expected number of columns.

---

### ✅ Valid Payload (Success Case)

```sql
' UNION SELECT 2, 'admin'--
```

**Why it works:**

* Matches the correct number of columns (2)
* Column data types align

---

### 📸 Screenshots

📤 **Client Input:** `' UNION SELECT 2, 'admin'--`
📥 **Server Response:** `Welcome admin!`

(Optional image references would go here)

---

### 🛡️ Reporting Format

**Title:** UNION-Based SQL Injection on login parameter

**Severity:** High
**Endpoint:** `POST /login`

**Steps to Reproduce:**

1. Go to login form
2. Enter username:

```sql
' UNION SELECT 2, 'admin'--
```

3. Observe admin access or leaked usernames

**Impact:**

* Unauthorized data access
* Potential account takeover

**Fix Recommendation:**

* Use parameterized queries (e.g., `?` placeholders)
* Sanitize user input strictly

---

### 🕵️ Attribution / Real-World Cases

* **MITRE ATT\&CK ID:** T1190 (Exploit Public-Facing Application)
* **Group Examples:** [TA505](https://attack.mitre.org/groups/G0092/), [FIN7](https://attack.mitre.org/groups/G0046/)

---

### 🎯 Final Thoughts

* UNION SQLi is only one of many SQL injection types.
* Detection often requires trial and error.
* Real bug bounty hunters take time to craft and refine their approach.

Keep pushing. You’re one payload closer to a real find.

---
