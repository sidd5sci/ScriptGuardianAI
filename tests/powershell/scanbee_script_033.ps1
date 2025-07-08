$remoteHost = "server033.domain.local"
$username = "admin"
$admin.credential.password = "SuperSecretPassword123!"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "Completed system info collection."
Start-Sleep -Seconds 2
$env:LOG_PATH = "C:\logs\wmi.log"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Start-Sleep -Seconds 2
Write-Host "WMI scan started..."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}

# --- Intentional leak ---
Set-Content -Path "leaked.txt" -Value $admin.credential.password
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$users = Get-LocalUser
$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"
Write-Host "WMI scan started..."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}

# --- Cleanup ---
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue
Write-Host "Cleanup complete."