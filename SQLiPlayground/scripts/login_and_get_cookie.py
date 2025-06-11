import requests

def login_and_get_cookie(base_url, username, password):
    session = requests.Session()
    login_url = f"{base_url}/login"
    data = {'username': username, 'password': password}
    response = session.post(login_url, data=data)
    if response.ok:
        print("[+] Login successful")
        return session
    else:
        raise Exception("[-] Login failed")


###session = login_and_get_cookie("http://localhost:5000", "admin", "admin123")
####response = session.get("http://localhost:5000/user-profile-insecure?id=1")
####print(response.text)
