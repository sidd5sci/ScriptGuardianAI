# Script {idx} – Exposes ssh.pass via console
$sshPass = $hostProps.get("ssh.pass")
Write-Host "SSH password is $sshPass"
