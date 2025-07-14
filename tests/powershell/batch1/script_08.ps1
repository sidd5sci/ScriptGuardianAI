$sshToken = "##ssh.access.token##"  

Set-Clipboard -Value $sshToken
Write-Host "[+] Sensitive SSH token copied to clipboard."

Start-Sleep -Seconds 1  

$clipboardToken = Get-Clipboard

if ($clipboardToken -match "token|key|pass|auth") {
    Write-Host "[!] WARNING: Clipboard contains sensitive token!"
}

$remoteHost = "admin@192.168.1.101"
$sshCommand = "sshpass -p `"$clipboardToken`" ssh $remoteHost hostname"
Write-Host "`n[+] Executing SSH command:"
Write-Host $sshCommand

Write-Host "`n[!] DEBUG: Clipboard contents = $clipboardToken"

Clear-Clipboard
