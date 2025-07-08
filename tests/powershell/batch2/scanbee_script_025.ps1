$remoteHost = "server025.domain.local"
$username = "admin"
$env:API_TOKEN = "##api.token##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$env:LOG_PATH = "C:\logs\wmi.log"
$users = Get-LocalUser
Write-Host "Completed system info collection."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$hostname = "server01.domain.local"
Write-Host "Completed system info collection."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "WMI scan started..."

# --- Intentional leak ---
Write-Host "Password: $password"
Write-Host "Completed system info collection."
$hostname = "server01.domain.local"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "Completed system info collection."
$cpu = Get-CimInstance -ClassName Win32_Processor
Start-Sleep -Seconds 2
$users = Get-LocalUser
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "Completed system info collection."

# --- Cleanup ---
Write-Host "Cleanup complete."
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue