$remoteHost = "server023.domain.local"
$username = "admin"
$azure.secret = "##azure.secretkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$hostname = "server01.domain.local"
$hostname = "server01.domain.local"
$users = Get-LocalUser
Write-Host "Completed system info collection."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$cpu = Get-CimInstance -ClassName Win32_Processor
$hostname = "server01.domain.local"

# --- Intentional leak ---
Write-Host "SNMP Auth used: $snmp.auth"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "Completed system info collection."
Write-Host "WMI scan started..."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$cpu = Get-CimInstance -ClassName Win32_Processor
$hostname = "server01.domain.local"
$users = Get-LocalUser
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "WMI scan started..."
Start-Sleep -Seconds 2

# --- Cleanup ---
Write-Host "Cleanup complete."
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue