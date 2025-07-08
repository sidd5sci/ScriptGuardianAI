$remoteHost = "server092.domain.local"
$username = "admin"
$gcp.key = "##gcp.serviceaccountkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$users = Get-LocalUser
$cpu = Get-CimInstance -ClassName Win32_Processor
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"
Write-Host "Completed system info collection."

# --- Intentional leak ---
Write-Host "SNMP Auth used: $snmp.auth"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$cpu = Get-CimInstance -ClassName Win32_Processor
Start-Sleep -Seconds 2
$cpu = Get-CimInstance -ClassName Win32_Processor
$env:LOG_PATH = "C:\logs\wmi.log"
$env:LOG_PATH = "C:\logs\wmi.log"
Start-Sleep -Seconds 2
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "WMI scan started..."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}

# --- Cleanup ---
Write-Host "Cleanup complete."
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue