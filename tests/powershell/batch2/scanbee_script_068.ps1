$remoteHost = "server068.domain.local"
$username = "admin"
$azure.secret = "##azure.secretkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$hostname = "server01.domain.local"
$hostname = "server01.domain.local"
$users = Get-LocalUser
Write-Host "Completed system info collection."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"

# --- Intentional leak ---
Write-Host "SNMP Auth used: $snmp.auth"
$users = Get-LocalUser
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$env:LOG_PATH = "C:\logs\wmi.log"
Start-Sleep -Seconds 2
$cpu = Get-CimInstance -ClassName Win32_Processor
$hostname = "server01.domain.local"
Write-Host "WMI scan started..."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "Completed system info collection."

# --- Cleanup ---
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue
Write-Host "Cleanup complete."