#!/bin/bash
# lfi_pipeline.sh
# Automated LFI Bug Bounty Workflow Script

TARGET_FILE="targets.txt"
SCAN_RESULTS="lfi_scan_results.txt"
HITS_FILE="lfi_hits.txt"
TARGET_URL="http://target.com/view"

echo "[*] Starting automated LFI testing pipeline..."

# Step 1: Clear old outputs
rm -f $SCAN_RESULTS $HITS_FILE LFI_Report_*.md

# Step 2: LFI Scanning
while read url; do
    echo "[*] Scanning $url"
    python3 lfi_scanner.py "$url" >> $SCAN_RESULTS
done < $TARGET_FILE

# Step 3: Filter hits
grep "Potential LFI found" $SCAN_RESULTS | tee $HITS_FILE

# Step 4: Generate report
i=1
while read line; do
    PAYLOAD=$(echo $line | cut -d':' -f2- | xargs)
    python3 lfi_reporter.py "$TARGET_URL" "$PAYLOAD"
    mv LFI_Report.md LFI_Report_$i.md
    i=$((i + 1))
done < $HITS_FILE

echo "[+] Pipeline complete. Reports saved as LFI_Report_*.md"
