$remoteHost = "server020.domain.local"
$username = "admin"
$password = "##wmi.pass##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "Completed system info collection."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$users = Get-LocalUser
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"
$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"
$hostname = "server01.domain.local"

# --- Intentional leak ---
Write-Host "SNMP Auth used: $snmp.auth"
$cpu = Get-CimInstance -ClassName Win32_Processor
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Start-Sleep -Seconds 2
Write-Host "WMI scan started..."
$env:LOG_PATH = "C:\logs\wmi.log"
$users = Get-LocalUser
$users = Get-LocalUser
$env:LOG_PATH = "C:\logs\wmi.log"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Cleanup ---
Write-Host "Cleanup complete."
Clear-Clipboard