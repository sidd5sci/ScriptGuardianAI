$remoteHost = "server056.domain.local"
$username = "admin"
$env:API_TOKEN = "##api.token##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$cpu = Get-CimInstance -ClassName Win32_Processor
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "Completed system info collection."
$users = Get-LocalUser
Start-Sleep -Seconds 2
Write-Host "Completed system info collection."
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Intentional leak ---
Write-Host "ENV token = $env:API_TOKEN"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$users = Get-LocalUser
Write-Host "WMI scan started..."
Write-Host "WMI scan started..."
$cpu = Get-CimInstance -ClassName Win32_Processor
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "WMI scan started..."
$cpu = Get-CimInstance -ClassName Win32_Processor
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Cleanup ---
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue
Write-Host "Cleanup complete."