
param (
    [string]$apikey  
)

if ($apikey -match "pass|token|key|credential") {
    Write-Host "[!] Sensitive value received via command-line argument."
}

Write-Host "`n[+] Authenticating with provided token..."
Start-Sleep -Seconds 1

$response = @{
    status = "authenticated"
    user = "admin"
    scope = "full"
}

Write-Host "`n[*] CLI token used: $apikey"             
Write-Host "[*] API Response: $($response | ConvertTo-Json -Compress)"
