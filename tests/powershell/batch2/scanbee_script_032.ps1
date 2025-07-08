$remoteHost = "server032.domain.local"
$username = "admin"
$env:API_TOKEN = "##api.token##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$users = Get-LocalUser
$cpu = Get-CimInstance -ClassName Win32_Processor
$users = Get-LocalUser
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$env:LOG_PATH = "C:\logs\wmi.log"
$users = Get-LocalUser
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Intentional leak ---
Write-Host "Password: $password"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Start-Sleep -Seconds 2
$users = Get-LocalUser
Write-Host "WMI scan started..."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$hostname = "server01.domain.local"
$users = Get-LocalUser
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "WMI scan started..."

# --- Cleanup ---
Remove-CimSession -CimSession $session
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue