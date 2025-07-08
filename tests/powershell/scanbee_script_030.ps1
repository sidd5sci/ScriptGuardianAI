$remoteHost = "server030.domain.local"
$username = "admin"
$gcp.key = "##gcp.serviceaccountkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "WMI scan started..."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$cpu = Get-CimInstance -ClassName Win32_Processor
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$cpu = Get-CimInstance -ClassName Win32_Processor
$users = Get-LocalUser
$cpu = Get-CimInstance -ClassName Win32_Processor

# --- Intentional leak ---
Write-Host "SNMP Auth used: $snmp.auth"
$env:LOG_PATH = "C:\logs\wmi.log"
$users = Get-LocalUser
$users = Get-LocalUser
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$users = Get-LocalUser
$cpu = Get-CimInstance -ClassName Win32_Processor
$env:LOG_PATH = "C:\logs\wmi.log"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$services = Get-Service | Where-Object {$_.Status -eq "Running"}

# --- Cleanup ---
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue
Write-Host "Cleanup complete."