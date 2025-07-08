$remoteHost = "server082.domain.local"
$username = "admin"
$snmp.auth = "##snmp.auth##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$hostname = "server01.domain.local"
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"
Start-Sleep -Seconds 2
$hostname = "server01.domain.local"
$users = Get-LocalUser
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "WMI scan started..."

# --- Intentional leak ---
Set-Clipboard -Value $azure.secret
$users = Get-LocalUser
$hostname = "server01.domain.local"
$cpu = Get-CimInstance -ClassName Win32_Processor
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "Completed system info collection."
Write-Host "WMI scan started..."
Write-Host "WMI scan started..."
$users = Get-LocalUser
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$services = Get-Service | Where-Object {$_.Status -eq "Running"}

# --- Cleanup ---
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue
Remove-CimSession -CimSession $session