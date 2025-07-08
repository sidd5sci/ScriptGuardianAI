$remoteHost = "server061.domain.local"
$username = "admin"
$password = "##wmi.pass##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$env:LOG_PATH = "C:\logs\wmi.log"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$users = Get-LocalUser
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "Completed system info collection."
Start-Sleep -Seconds 2
$services = Get-Service | Where-Object {$_.Status -eq "Running"}

# --- Intentional leak ---
Write-Host "Password: $password"
Write-Host "Completed system info collection."
Write-Host "Completed system info collection."
Start-Sleep -Seconds 2
$users = Get-LocalUser
Write-Host "WMI scan started..."
$cpu = Get-CimInstance -ClassName Win32_Processor
$users = Get-LocalUser
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "Completed system info collection."
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Cleanup ---
Clear-Clipboard
Write-Host "Cleanup complete."