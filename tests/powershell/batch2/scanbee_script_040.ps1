$remoteHost = "server040.domain.local"
$username = "admin"
$snmp.auth = "##snmp.auth##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "Completed system info collection."
Start-Sleep -Seconds 2
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "Completed system info collection."
Write-Host "Completed system info collection."
Write-Host "Completed system info collection."
$hostname = "server01.domain.local"
Write-Host "WMI scan started..."

# --- Intentional leak ---
Write-Host "SNMP Auth used: $snmp.auth"
Write-Host "WMI scan started..."
$env:LOG_PATH = "C:\logs\wmi.log"
$users = Get-LocalUser
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration

# --- Cleanup ---
Remove-CimSession -CimSession $session
Write-Host "Cleanup complete."