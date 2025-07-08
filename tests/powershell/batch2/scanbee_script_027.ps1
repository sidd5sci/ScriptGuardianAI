$remoteHost = "server027.domain.local"
$username = "admin"
$admin.credential.password = "SuperSecretPassword123!"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "Completed system info collection."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$hostname = "server01.domain.local"
$users = Get-LocalUser
$cpu = Get-CimInstance -ClassName Win32_Processor
$env:LOG_PATH = "C:\logs\wmi.log"
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Intentional leak ---
Write-Host "Password: $password"
Start-Sleep -Seconds 2
Write-Host "WMI scan started..."
$hostname = "server01.domain.local"
Write-Host "WMI scan started..."
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "WMI scan started..."
Write-Host "Completed system info collection."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Cleanup ---
Write-Host "Cleanup complete."
Remove-CimSession -CimSession $session