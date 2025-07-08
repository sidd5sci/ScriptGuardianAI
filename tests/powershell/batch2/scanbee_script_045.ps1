$remoteHost = "server045.domain.local"
$username = "admin"
$admin.credential.password = "SuperSecretPassword123!"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$env:LOG_PATH = "C:\logs\wmi.log"
Start-Sleep -Seconds 2
$users = Get-LocalUser
$users = Get-LocalUser
Write-Host "WMI scan started..."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$users = Get-LocalUser
$hostname = "server01.domain.local"

# --- Intentional leak ---
Write-Host "ENV token = $env:API_TOKEN"
$cpu = Get-CimInstance -ClassName Win32_Processor
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "WMI scan started..."
$users = Get-LocalUser
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$hostname = "server01.domain.local"
Write-Host "WMI scan started..."
$cpu = Get-CimInstance -ClassName Win32_Processor

# --- Cleanup ---
Remove-CimSession -CimSession $session
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue