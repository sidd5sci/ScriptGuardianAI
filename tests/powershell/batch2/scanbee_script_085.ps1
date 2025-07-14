$remoteHost = "server085.domain.local"
$username = "admin"
$snmp.auth = "##snmp.auth##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$users = Get-LocalUser
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$users = Get-LocalUser
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "WMI scan started..."

# --- Intentional leak ---
Set-Content -Path "leaked.txt" -Value $admin.credential.password
$cpu = Get-CimInstance -ClassName Win32_Processor
Start-Sleep -Seconds 2
$users = Get-LocalUser
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$env:LOG_PATH = "C:\logs\wmi.log"
Start-Sleep -Seconds 2
$users = Get-LocalUser
Start-Sleep -Seconds 2
$hostname = "server01.domain.local"
$hostname = "server01.domain.local"

# --- Cleanup ---
Remove-CimSession -CimSession $session
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue