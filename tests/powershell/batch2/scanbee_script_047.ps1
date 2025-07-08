$remoteHost = "server047.domain.local"
$username = "admin"
$snmp.auth = "##snmp.auth##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "WMI scan started..."
$users = Get-LocalUser
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "Completed system info collection."
$cpu = Get-CimInstance -ClassName Win32_Processor
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "WMI scan started..."
$users = Get-LocalUser

# --- Intentional leak ---
Set-Content -Path "leaked.txt" -Value $admin.credential.password
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "Completed system info collection."
Write-Host "Completed system info collection."
$users = Get-LocalUser
$hostname = "server01.domain.local"
$users = Get-LocalUser
Write-Host "WMI scan started..."
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "WMI scan started..."
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Cleanup ---
Clear-Clipboard
Write-Host "Cleanup complete."