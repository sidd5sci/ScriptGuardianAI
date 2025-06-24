# ================================
# Simulated Command-Line Argument Leak (password/token)
# ================================

param (
    [string]$apikey  # Accepts --apikey=... or positional argument
)

# Simulate detection of sensitive CLI input
if ($apikey -match "pass|token|key|credential") {
    Write-Host "[!] Sensitive value received via command-line argument."
}

# Simulated sensitive processing
Write-Host "`n[+] Authenticating with provided token..."
Start-Sleep -Seconds 1

# Simulate result of using the API key
$response = @{
    status = "authenticated"
    user = "admin"
    scope = "full"
}

# LEAK: Print sensitive input along with result
Write-Host "`n[*] CLI token used: $apikey"              # 🚨 Console leak
Write-Host "[*] API Response: $($response | ConvertTo-Json -Compress)"
