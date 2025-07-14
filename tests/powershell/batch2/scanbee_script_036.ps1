$remoteHost = "server036.domain.local"
$username = "admin"
$password = "##wmi.pass##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$env:LOG_PATH = "C:\logs\wmi.log"
$users = Get-LocalUser
Write-Host "Completed system info collection."
$hostname = "server01.domain.local"
$hostname = "server01.domain.local"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$users = Get-LocalUser
Write-Host "WMI scan started..."

# --- Intentional leak ---
Write-Host "Password: $password"
$cpu = Get-CimInstance -ClassName Win32_Processor
$env:LOG_PATH = "C:\logs\wmi.log"
Start-Sleep -Seconds 2
Start-Sleep -Seconds 2
$cpu = Get-CimInstance -ClassName Win32_Processor
$hostname = "server01.domain.local"
$cpu = Get-CimInstance -ClassName Win32_Processor
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "Completed system info collection."
Write-Host "WMI scan started..."

# --- Cleanup ---
Write-Host "Cleanup complete."
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue