$env:SSH_PASS = "##ssh.connection.password##"  

$remoteUser = "admin"
$remoteHost = "192.168.1.100"

$sshCommand = "sshpass -p `"$env:SSH_PASS`" ssh $remoteUser@$remoteHost 'hostname'"

Write-Host "[+] Executing SSH command: $sshCommand"
Invoke-Expression $sshCommand

Write-Host "[!] For debug: SSH password = $env:SSH_PASS"

Remove-Item Env:SSH_PASS
