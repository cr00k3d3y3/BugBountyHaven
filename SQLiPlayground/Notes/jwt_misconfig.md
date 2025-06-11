🧪 Challenge Flow

    1. User logs in at /jwt_login as a normal user.

    2. Attacker decodes the JWT (base64), modifies role to    admin, and re-signs it.

    3. They replace the cookie and access /jwt_admin.

    4. ✅ Flag is revealed.


    # 🔓 JWT Token Role Escalation

## 🎯 Objective

Exploit weak JWT protection to escalate from user to admin.

---

## 🧠 Application Context

- `/jwt_login`: Accepts any username, issues a signed JWT with a hardcoded secret (`HS256`).
- `/jwt_admin`: Accepts JWT cookie and grants admin access if `role` is `admin`.

---

## 🧪 Exploitation Steps

### Step 1: Login as a Normal User

Visit:
http://localhost:8081/jwt_login

Username: guest



Copy the token shown (stored in `jwt` cookie).

---

### Step 2: Decode the JWT

Run pyjwt.py

import jwt

payload = {
    "user": "guest",
    "role": "admin"
}

secret = "wrong-secret"

token = jwt.encode(payload, secret, algorithm="HS256")
print(token)



Step 3: Modify and Re-sign

Change role to admin in the payload.

Use a weak secret to re-sign (ultraweaksecret, algorithm HS256).

Step 4: Replace JWT Cookie

Use browser dev tools to overwrite the cookie:

jwt=eyJhbGciOi...

Step 5: Access Protected Admin Area

Visit:  http://localhost:8081/jwt_admin


You should see:

🎉 FLAG{jwt_token_tampering}

✅ Takeaways

    JWTs with weak secrets are dangerous

    Role escalation is possible with client-controlled tokens

    Never trust client-side data for access control
