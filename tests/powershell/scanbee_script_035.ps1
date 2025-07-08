$remoteHost = "server035.domain.local"
$username = "admin"
$snmp.auth = "##snmp.auth##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Start-Sleep -Seconds 2
$hostname = "server01.domain.local"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$users = Get-LocalUser
Write-Host "WMI scan started..."
Write-Host "Completed system info collection."
$hostname = "server01.domain.local"

# --- Intentional leak ---
Set-Content -Path "leaked.txt" -Value $admin.credential.password
$hostname = "server01.domain.local"
Start-Sleep -Seconds 2
$users = Get-LocalUser
$hostname = "server01.domain.local"
$hostname = "server01.domain.local"
Start-Sleep -Seconds 2
Write-Host "Completed system info collection."
$hostname = "server01.domain.local"
Start-Sleep -Seconds 2
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Cleanup ---
Remove-CimSession -CimSession $session
Clear-Clipboard