$remoteHost = "server029.domain.local"
$username = "admin"
$snmp.auth = "##snmp.auth##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$hostname = "server01.domain.local"
$users = Get-LocalUser
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "WMI scan started..."
$hostname = "server01.domain.local"

# --- Intentional leak ---
Write-Host "ENV token = $env:API_TOKEN"
Start-Sleep -Seconds 2
$hostname = "server01.domain.local"
Start-Sleep -Seconds 2
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "WMI scan started..."
$users = Get-LocalUser
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "Completed system info collection."
Write-Host "WMI scan started..."
$users = Get-LocalUser

# --- Cleanup ---
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue
Remove-CimSession -CimSession $session