$remoteHost = "server052.domain.local"
$username = "admin"
$admin.credential.password = "SuperSecretPassword123!"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$env:LOG_PATH = "C:\logs\wmi.log"
$users = Get-LocalUser
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "Completed system info collection."
Start-Sleep -Seconds 2
Write-Host "Completed system info collection."
$hostname = "server01.domain.local"
$users = Get-LocalUser

# --- Intentional leak ---
Write-Host "ENV token = $env:API_TOKEN"
$env:LOG_PATH = "C:\logs\wmi.log"
Start-Sleep -Seconds 2
$users = Get-LocalUser
$cpu = Get-CimInstance -ClassName Win32_Processor
Start-Sleep -Seconds 2
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$users = Get-LocalUser
$users = Get-LocalUser
Write-Host "Completed system info collection."

# --- Cleanup ---
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue
Clear-Clipboard