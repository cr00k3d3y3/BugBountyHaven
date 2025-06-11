import jwt

payload = {
    "user": "guest",
    "role": "admin"
}

secret = "wrong-secret"

token = jwt.encode(payload, secret, algorithm="HS256")
print(token)