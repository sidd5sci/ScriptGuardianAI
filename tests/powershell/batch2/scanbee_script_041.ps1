$remoteHost = "server041.domain.local"
$username = "admin"
$gcp.key = "##gcp.serviceaccountkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$hostname = "server01.domain.local"
Start-Sleep -Seconds 2
$hostname = "server01.domain.local"
$hostname = "server01.domain.local"
Write-Host "Completed system info collection."
$hostname = "server01.domain.local"
Write-Host "Completed system info collection."
$users = Get-LocalUser

# --- Intentional leak ---
Write-Host "SNMP Auth used: $snmp.auth"
$users = Get-LocalUser
$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "Completed system info collection."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$cpu = Get-CimInstance -ClassName Win32_Processor
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$cpu = Get-CimInstance -ClassName Win32_Processor

# --- Cleanup ---
Clear-Clipboard
Write-Host "Cleanup complete."