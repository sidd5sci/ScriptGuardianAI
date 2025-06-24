# Script {idx} – Copies secret to another variable then prints
$secret = $hostProps["ssh.pass"]
$leak = $secret
Write-Host $leak
