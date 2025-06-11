#!/usr/bin/env python3
"""
LFI RCE Flag Detector Script
----------------------------

🔍 PURPOSE:
This script scans the `shell_logs.txt` file produced by the logging reverse shell
(`shell.php`) deployed in the LFIWebApp. It looks for a specific flag access pattern,
such as reading /tmp/.flag, to simulate real-world detection of attacker behavior.

🛠 WHEN TO USE:
- After deploying `shell.php` in `uploads/` with logging functionality
- After you have triggered one or more commands (via browser or reverse shell)
- Anytime you want to audit what commands have been run during exploitation

📌 WHAT TO EXPECT:
- If a matching flag-read pattern is found, the script prints it and simulates scoring
- If no match is found, the script will let you know, but still list all commands run

🚫 WHAT NOT TO EXPECT:
- This script does not exploit or interact with the web server
- It assumes `shell_logs.txt` is present in the local `uploads/` directory

⚠️ REQUIREMENTS:
- Run this script from the same directory that contains `uploads/shell_logs.txt`
- Must have Python 3.x

"""

import os

log_path = "uploads/shell_logs.txt"
flag_patterns = ["cat /tmp/.flag", "cat /flag", "cat /root/flag", "less /tmp/.flag", "curl .*flag.*"]

if not os.path.exists(log_path):
    print(f"❌ Log file not found: {log_path}")
    exit(1)

print(f"🔍 Scanning {log_path} for flag access attempts...\n")

with open(log_path, "r") as f:
    lines = f.readlines()

found_flag = False

for line in lines:
    timestamp, _, cmd = line.partition(" | ")
    cmd = cmd.strip()
    if any(pattern in cmd for pattern in flag_patterns):
        print(f"🚩 FLAG ACCESS DETECTED at {timestamp.strip()} → `{cmd}`")
        found_flag = True

if not found_flag:
    print("✅ No flag retrieval attempts detected.")

print("\n📜 Full command history:")
for line in lines:
    print("  " + line.strip())
