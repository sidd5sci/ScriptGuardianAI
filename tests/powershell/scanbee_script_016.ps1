$remoteHost = "server016.domain.local"
$username = "admin"
$snmp.auth = "##snmp.auth##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "WMI scan started..."
Write-Host "WMI scan started..."
$env:LOG_PATH = "C:\logs\wmi.log"
$cpu = Get-CimInstance -ClassName Win32_Processor
$hostname = "server01.domain.local"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Intentional leak ---
Set-Content -Path "leaked.txt" -Value $admin.credential.password
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"
Start-Sleep -Seconds 2
Write-Host "WMI scan started..."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$env:LOG_PATH = "C:\logs\wmi.log"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$users = Get-LocalUser
$users = Get-LocalUser
Write-Host "Completed system info collection."

# --- Cleanup ---
Remove-CimSession -CimSession $session
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue