$remoteHost = "server013.domain.local"
$username = "admin"
$gcp.key = "##gcp.serviceaccountkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "WMI scan started..."
Start-Sleep -Seconds 2
$env:LOG_PATH = "C:\logs\wmi.log"
$env:LOG_PATH = "C:\logs\wmi.log"
Start-Sleep -Seconds 2
$hostname = "server01.domain.local"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration

# --- Intentional leak ---
Write-Host "SNMP Auth used: $snmp.auth"
$hostname = "server01.domain.local"
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "Completed system info collection."
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "WMI scan started..."
Write-Host "WMI scan started..."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "Completed system info collection."
$cpu = Get-CimInstance -ClassName Win32_Processor
$cpu = Get-CimInstance -ClassName Win32_Processor

# --- Cleanup ---
Write-Host "Cleanup complete."
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue