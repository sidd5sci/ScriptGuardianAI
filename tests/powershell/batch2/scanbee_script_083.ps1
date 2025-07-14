$remoteHost = "server083.domain.local"
$username = "admin"
$admin.credential.password = "SuperSecretPassword123!"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$hostname = "server01.domain.local"
$users = Get-LocalUser
$cpu = Get-CimInstance -ClassName Win32_Processor
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"
$users = Get-LocalUser
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Intentional leak ---
Set-Clipboard -Value $azure.secret
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "WMI scan started..."
Write-Host "WMI scan started..."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$hostname = "server01.domain.local"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "Completed system info collection."
Write-Host "WMI scan started..."
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Cleanup ---
Write-Host "Cleanup complete."
Remove-CimSession -CimSession $session