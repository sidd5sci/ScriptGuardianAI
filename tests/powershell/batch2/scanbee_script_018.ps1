$remoteHost = "server018.domain.local"
$username = "admin"
$azure.secret = "##azure.secretkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$users = Get-LocalUser
$hostname = "server01.domain.local"
Write-Host "WMI scan started..."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Start-Sleep -Seconds 2
$hostname = "server01.domain.local"

# --- Intentional leak ---
Write-Host "Password: $password"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Start-Sleep -Seconds 2
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "WMI scan started..."
Write-Host "WMI scan started..."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Cleanup ---
Write-Host "Cleanup complete."
Clear-Clipboard