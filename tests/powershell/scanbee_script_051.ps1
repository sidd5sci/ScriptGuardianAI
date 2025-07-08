$remoteHost = "server051.domain.local"
$username = "admin"
$azure.secret = "##azure.secretkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "WMI scan started..."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$cpu = Get-CimInstance -ClassName Win32_Processor
$cpu = Get-CimInstance -ClassName Win32_Processor
$env:LOG_PATH = "C:\logs\wmi.log"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$hostname = "server01.domain.local"
$users = Get-LocalUser

# --- Intentional leak ---
Write-Host "ENV token = $env:API_TOKEN"
Write-Host "WMI scan started..."
Write-Host "Completed system info collection."
Write-Host "Completed system info collection."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "Completed system info collection."
$hostname = "server01.domain.local"
Start-Sleep -Seconds 2
Write-Host "Completed system info collection."
$env:LOG_PATH = "C:\logs\wmi.log"
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Cleanup ---
Clear-Clipboard
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue