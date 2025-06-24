# ================================
# Simulated SSH Connection via Env Variable Leak
# ================================

# Step 1: Store sensitive SSH password in environment variable
$env:SSH_PASS = "##ssh.connection.password##"  # ✅ matches regex: .*password$

# Step 2: Prepare SSH command (Note: Simulated for test environment)
$remoteUser = "admin"
$remoteHost = "192.168.1.100"

# WARNING: Normally you'd use SSH key auth — password injection like this is insecure
$sshCommand = "sshpass -p `"$env:SSH_PASS`" ssh $remoteUser@$remoteHost 'hostname'"

# Step 3: Execute SSH (simulated, not secure)
Write-Host "[+] Executing SSH command: $sshCommand"
Invoke-Expression $sshCommand

# Optional Leak: echo password to console (to test console leak detection)
Write-Host "[!] For debug: SSH password = $env:SSH_PASS"

# Cleanup
Remove-Item Env:SSH_PASS
