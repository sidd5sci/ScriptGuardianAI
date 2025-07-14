$remoteHost = "server050.domain.local"
$username = "admin"
$gcp.key = "##gcp.serviceaccountkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Start-Sleep -Seconds 2
$hostname = "server01.domain.local"
$users = Get-LocalUser
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Start-Sleep -Seconds 2
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$cpu = Get-CimInstance -ClassName Win32_Processor

# --- Intentional leak ---
Write-Host "Password: $password"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "Completed system info collection."
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "Completed system info collection."
$hostname = "server01.domain.local"
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"
$users = Get-LocalUser
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Cleanup ---
Remove-CimSession -CimSession $session
Clear-Clipboard