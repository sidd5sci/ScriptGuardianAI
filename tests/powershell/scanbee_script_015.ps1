$remoteHost = "server015.domain.local"
$username = "admin"
$gcp.key = "##gcp.serviceaccountkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "Completed system info collection."
$env:LOG_PATH = "C:\logs\wmi.log"
$cpu = Get-CimInstance -ClassName Win32_Processor
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$cpu = Get-CimInstance -ClassName Win32_Processor
Start-Sleep -Seconds 2
$users = Get-LocalUser
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Intentional leak ---
Write-Host "ENV token = $env:API_TOKEN"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "WMI scan started..."
Start-Sleep -Seconds 2
$env:LOG_PATH = "C:\logs\wmi.log"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$hostname = "server01.domain.local"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Start-Sleep -Seconds 2

# --- Cleanup ---
Remove-CimSession -CimSession $session
Write-Host "Cleanup complete."