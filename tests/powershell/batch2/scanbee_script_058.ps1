$remoteHost = "server058.domain.local"
$username = "admin"
$snmp.auth = "##snmp.auth##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "WMI scan started..."
Write-Host "WMI scan started..."
$users = Get-LocalUser
Write-Host "Completed system info collection."
Write-Host "WMI scan started..."
Write-Host "WMI scan started..."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Intentional leak ---
Set-Clipboard -Value $azure.secret
Write-Host "WMI scan started..."
$cpu = Get-CimInstance -ClassName Win32_Processor
$users = Get-LocalUser
Start-Sleep -Seconds 2
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$hostname = "server01.domain.local"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$services = Get-Service | Where-Object {$_.Status -eq "Running"}

# --- Cleanup ---
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue
Write-Host "Cleanup complete."