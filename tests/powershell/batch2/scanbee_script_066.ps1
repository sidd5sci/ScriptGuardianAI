$remoteHost = "server066.domain.local"
$username = "admin"
$azure.secret = "##azure.secretkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "Completed system info collection."
$users = Get-LocalUser
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$env:LOG_PATH = "C:\logs\wmi.log"
$cpu = Get-CimInstance -ClassName Win32_Processor
Start-Sleep -Seconds 2
$hostname = "server01.domain.local"

# --- Intentional leak ---
Write-Host "ENV token = $env:API_TOKEN"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$users = Get-LocalUser
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$hostname = "server01.domain.local"
Write-Host "Completed system info collection."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "WMI scan started..."
$users = Get-LocalUser
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Cleanup ---
Write-Host "Cleanup complete."
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue