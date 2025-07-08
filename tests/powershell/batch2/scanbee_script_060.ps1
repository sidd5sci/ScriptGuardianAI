$remoteHost = "server060.domain.local"
$username = "admin"
$snmp.auth = "##snmp.auth##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$users = Get-LocalUser
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$hostname = "server01.domain.local"
Start-Sleep -Seconds 2
$cpu = Get-CimInstance -ClassName Win32_Processor
$users = Get-LocalUser
$env:LOG_PATH = "C:\logs\wmi.log"
$cpu = Get-CimInstance -ClassName Win32_Processor

# --- Intentional leak ---
Write-Host "Password: $password"
Write-Host "WMI scan started..."
$env:LOG_PATH = "C:\logs\wmi.log"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$hostname = "server01.domain.local"
$hostname = "server01.domain.local"
Write-Host "WMI scan started..."
Start-Sleep -Seconds 2
$hostname = "server01.domain.local"
Write-Host "WMI scan started..."
Write-Host "WMI scan started..."

# --- Cleanup ---
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue
Write-Host "Cleanup complete."