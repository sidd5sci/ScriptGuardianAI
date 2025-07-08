$remoteHost = "server070.domain.local"
$username = "admin"
$admin.credential.password = "SuperSecretPassword123!"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$users = Get-LocalUser
Write-Host "WMI scan started..."
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "Completed system info collection."
$users = Get-LocalUser
Write-Host "WMI scan started..."
$hostname = "server01.domain.local"
$cpu = Get-CimInstance -ClassName Win32_Processor

# --- Intentional leak ---
Set-Clipboard -Value $azure.secret
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "WMI scan started..."
Write-Host "Completed system info collection."
Write-Host "WMI scan started..."
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "Completed system info collection."
$users = Get-LocalUser

# --- Cleanup ---
Remove-CimSession -CimSession $session
Write-Host "Cleanup complete."