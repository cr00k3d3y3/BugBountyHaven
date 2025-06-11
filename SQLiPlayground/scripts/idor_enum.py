def enumerate_profiles(session, base_url, start_id=1, end_id=10):
    for uid in range(start_id, end_id + 1):
        url = f"{base_url}/user-profile-insecure?id={uid}"
        response = session.get(url)
        if "Username:" in response.text:
            print(f"[+] ID {uid} - Profile Found")
        else:
            print(f"[-] ID {uid} - Not Found")
