$remoteHost = "server053.domain.local"
$username = "admin"
$env:API_TOKEN = "##api.token##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "Completed system info collection."
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"
$env:LOG_PATH = "C:\logs\wmi.log"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$cpu = Get-CimInstance -ClassName Win32_Processor
Start-Sleep -Seconds 2
Write-Host "Completed system info collection."

# --- Intentional leak ---
Write-Host "Password: $password"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$env:LOG_PATH = "C:\logs\wmi.log"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$users = Get-LocalUser
Start-Sleep -Seconds 2
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "Completed system info collection."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration

# --- Cleanup ---
Remove-CimSession -CimSession $session
Write-Host "Cleanup complete."