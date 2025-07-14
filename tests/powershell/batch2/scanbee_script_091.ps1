$remoteHost = "server091.domain.local"
$username = "admin"
$azure.secret = "##azure.secretkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$cpu = Get-CimInstance -ClassName Win32_Processor
$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "Completed system info collection."
$cpu = Get-CimInstance -ClassName Win32_Processor
$hostname = "server01.domain.local"

# --- Intentional leak ---
Write-Host "SNMP Auth used: $snmp.auth"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$cpu = Get-CimInstance -ClassName Win32_Processor
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$hostname = "server01.domain.local"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "Completed system info collection."
Start-Sleep -Seconds 2
Write-Host "Completed system info collection."
Write-Host "Completed system info collection."
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Cleanup ---
Write-Host "Cleanup complete."
Remove-CimSession -CimSession $session