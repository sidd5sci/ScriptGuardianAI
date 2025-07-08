$remoteHost = "server055.domain.local"
$username = "admin"
$gcp.key = "##gcp.serviceaccountkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "WMI scan started..."
$env:LOG_PATH = "C:\logs\wmi.log"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$cpu = Get-CimInstance -ClassName Win32_Processor
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$users = Get-LocalUser
Start-Sleep -Seconds 2
Write-Host "Completed system info collection."

# --- Intentional leak ---
Write-Host "ENV token = $env:API_TOKEN"
$cpu = Get-CimInstance -ClassName Win32_Processor
$hostname = "server01.domain.local"
Start-Sleep -Seconds 2
$env:LOG_PATH = "C:\logs\wmi.log"
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "Completed system info collection."
$hostname = "server01.domain.local"
Start-Sleep -Seconds 2
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "Completed system info collection."

# --- Cleanup ---
Remove-CimSession -CimSession $session
Write-Host "Cleanup complete."