$remoteHost = "server004.domain.local"
$username = "admin"
$gcp.key = "##gcp.serviceaccountkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$users = Get-LocalUser
Start-Sleep -Seconds 2
$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"
Start-Sleep -Seconds 2
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration

# --- Intentional leak ---
Write-Host "ENV token = $env:API_TOKEN"
Start-Sleep -Seconds 2
Write-Host "WMI scan started..."
Write-Host "Completed system info collection."
$users = Get-LocalUser
$cpu = Get-CimInstance -ClassName Win32_Processor
$cpu = Get-CimInstance -ClassName Win32_Processor
Start-Sleep -Seconds 2
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Cleanup ---
Remove-CimSession -CimSession $session
Write-Host "Cleanup complete."