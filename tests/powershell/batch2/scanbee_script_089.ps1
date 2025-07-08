$remoteHost = "server089.domain.local"
$username = "admin"
$env:API_TOKEN = "##api.token##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "Completed system info collection."
Write-Host "WMI scan started..."
$hostname = "server01.domain.local"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Start-Sleep -Seconds 2
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Start-Sleep -Seconds 2
Write-Host "Completed system info collection."

# --- Intentional leak ---
Set-Clipboard -Value $azure.secret
$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"
Start-Sleep -Seconds 2
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "WMI scan started..."
$cpu = Get-CimInstance -ClassName Win32_Processor
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "Completed system info collection."
$hostname = "server01.domain.local"

# --- Cleanup ---
Remove-CimSession -CimSession $session
Write-Host "Cleanup complete."