$remoteHost = "server079.domain.local"
$username = "admin"
$password = "##wmi.pass##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"
$users = Get-LocalUser
Write-Host "WMI scan started..."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration

# --- Intentional leak ---
Set-Content -Path "leaked.txt" -Value $admin.credential.password
$hostname = "server01.domain.local"
$users = Get-LocalUser
Write-Host "WMI scan started..."
$hostname = "server01.domain.local"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "Completed system info collection."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$cpu = Get-CimInstance -ClassName Win32_Processor
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Start-Sleep -Seconds 2

# --- Cleanup ---
Clear-Clipboard
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue