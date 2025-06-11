# 🛡️ JWT Privilege Escalation

## 🎯 Objective

Exploit JWT misconfiguration to gain admin access.

---

## 🔍 Application Context

- **JWT Generation**: At `/jwt`, users are issued a signed JWT based on login credentials.
- **Access Control**: `/admin_jwt` checks for `role=admin` in the JWT payload.
- **Vulnerability**: Weak shared secret (`secret123`) allows token forgery.

---

## 🧪 Exploitation Steps

1. **Login as Any User**

   Go to `/jwt` and submit:

username: guest
password: guest


2. **Capture JWT Token**

Copy the issued JWT from the response.

3. **Forge Admin Token**

Use a tool like [jwt.io](https://jwt.io) or `jwt` CLI:
```bash
jwt encode --alg HS256 --secret secret123 '{"user":"admin","role":"admin"}'

Submit to Protected Endpoint

Use browser extensions or tools to add the header:

Authorization: Bearer <your_forged_token>

Access /jwt again with that header.

🎉 Success Condition

    Flag: FLAG{jwt_admin_forged} will appear on valid forgery.

    ✅ Defense

    Use strong JWT secrets.

    Prefer RS256 (asymmetric) algorithms.

    Do not store roles in JWT without backend verification.