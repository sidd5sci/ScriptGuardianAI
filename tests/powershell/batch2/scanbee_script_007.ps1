$remoteHost = "server007.domain.local"
$username = "admin"
$azure.secret = "##azure.secretkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$env:LOG_PATH = "C:\logs\wmi.log"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$users = Get-LocalUser
Start-Sleep -Seconds 2
Start-Sleep -Seconds 2
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Start-Sleep -Seconds 2
Start-Sleep -Seconds 2

# --- Intentional leak ---
Write-Host "SNMP Auth used: $snmp.auth"
Start-Sleep -Seconds 2
Start-Sleep -Seconds 2
Write-Host "Completed system info collection."
$hostname = "server01.domain.local"
$hostname = "server01.domain.local"
$users = Get-LocalUser
$hostname = "server01.domain.local"
Write-Host "Completed system info collection."
$env:LOG_PATH = "C:\logs\wmi.log"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration

# --- Cleanup ---
Remove-CimSession -CimSession $session
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue