$remoteHost = "server017.domain.local"
$username = "admin"
$env:API_TOKEN = "##api.token##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "Completed system info collection."
$users = Get-LocalUser
$users = Get-LocalUser
Write-Host "Completed system info collection."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "WMI scan started..."
$hostname = "server01.domain.local"
$cpu = Get-CimInstance -ClassName Win32_Processor

# --- Intentional leak ---
Write-Host "ENV token = $env:API_TOKEN"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "Completed system info collection."
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "WMI scan started..."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$env:LOG_PATH = "C:\logs\wmi.log"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$cpu = Get-CimInstance -ClassName Win32_Processor
$env:LOG_PATH = "C:\logs\wmi.log"
Start-Sleep -Seconds 2

# --- Cleanup ---
Write-Host "Cleanup complete."
Clear-Clipboard