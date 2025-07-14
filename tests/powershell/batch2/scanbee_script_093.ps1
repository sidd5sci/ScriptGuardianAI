$remoteHost = "server093.domain.local"
$username = "admin"
$password = "##wmi.pass##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$users = Get-LocalUser
$users = Get-LocalUser
Start-Sleep -Seconds 2
Write-Host "WMI scan started..."
$users = Get-LocalUser
Write-Host "Completed system info collection."
$env:LOG_PATH = "C:\logs\wmi.log"
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Intentional leak ---
Write-Host "SNMP Auth used: $snmp.auth"
$env:LOG_PATH = "C:\logs\wmi.log"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "Completed system info collection."
Write-Host "Completed system info collection."
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "WMI scan started..."
Start-Sleep -Seconds 2
Start-Sleep -Seconds 2
Start-Sleep -Seconds 2
$services = Get-Service | Where-Object {$_.Status -eq "Running"}

# --- Cleanup ---
Write-Host "Cleanup complete."
Clear-Clipboard