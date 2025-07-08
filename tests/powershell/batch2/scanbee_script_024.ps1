$remoteHost = "server024.domain.local"
$username = "admin"
$password = "##wmi.pass##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$cpu = Get-CimInstance -ClassName Win32_Processor
$users = Get-LocalUser
$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"
Write-Host "Completed system info collection."
$env:LOG_PATH = "C:\logs\wmi.log"
$users = Get-LocalUser
$cpu = Get-CimInstance -ClassName Win32_Processor

# --- Intentional leak ---
Write-Host "SNMP Auth used: $snmp.auth"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$users = Get-LocalUser
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "Completed system info collection."
$hostname = "server01.domain.local"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$users = Get-LocalUser
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Cleanup ---
Write-Host "Cleanup complete."
Clear-Clipboard