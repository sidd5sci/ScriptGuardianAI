# ===============================================
# Simulated SSH Connection Using Token from Clipboard
# ===============================================

# Step 1: Set up sensitive token
$sshToken = "##ssh.access.token##"  # 🔐 Matches regex: .*token$

# Step 2: Copy token to clipboard (clipboard leak)
Set-Clipboard -Value $sshToken
Write-Host "[+] Sensitive SSH token copied to clipboard."

# Step 3: Simulate SSH command using clipboard content
Start-Sleep -Seconds 1  # Simulate delay before SSH call

$clipboardToken = Get-Clipboard

# Optional detection
if ($clipboardToken -match "token|key|pass|auth") {
    Write-Host "[!] WARNING: Clipboard contains sensitive token!"
}

# Step 4: Simulate SSH using clipboard token (mocked command)
$remoteHost = "admin@192.168.1.101"
$sshCommand = "sshpass -p `"$clipboardToken`" ssh $remoteHost hostname"
Write-Host "`n[+] Executing SSH command:"
Write-Host $sshCommand

# Step 5: Print the clipboard content (Console leak)
Write-Host "`n[!] DEBUG: Clipboard contents = $clipboardToken"

# Cleanup (optional)
Clear-Clipboard
