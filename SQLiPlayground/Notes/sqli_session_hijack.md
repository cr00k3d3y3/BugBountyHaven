# 🧪 SQL Injection to Session Hijack Exploitation Chain

## 🎯 Objective
Simulate a real-world exploit chain:
1. **SQL Injection (Leak SessionID)**
2. **Session Hijacking (Cookie Manipulation)**
3. **Privilege Escalation to Admin**
4. **Flag Retrieval**

---

## 💥 1. Vulnerable Route: `/leak`

### Function:
Performs an unsafe query based on user input:
```python
query = f"SELECT * FROM users WHERE username = '{user}'"


Exploit:

Submit any valid user (e.g., admin) to simulate session ID leakage.

Example:

POST /leak
user=admin

Output:

Simulated leak: SESSIONID=admin_1

🔐 2. Simulate Session Hijack
Target:

@app.route('/admin')
def admin():
    if request.cookies.get('auth') == 'admin':
        return render_template('flag.html', flag="FLAG-1{Session_Hijack_Success}")
    return "Access Denied"


Exploit:

    Open browser DevTools

    Navigate to: Storage > Cookies > http://127.0.0.1:8081

    Add cookie:

        Name: auth

        Value: admin

Visit:

http://127.0.0.1:8081/admin

💡 Lessons for Bug Bounty

    Always check if exposed inputs lead to SQLi (even POST-only)

    Observe if user state or session data is indirectly exposed

    Test for cookie-based privilege checks

    Manual session cookie injection is a powerful escalation method