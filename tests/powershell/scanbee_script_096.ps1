$remoteHost = "server096.domain.local"
$username = "admin"
$password = "##wmi.pass##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "Completed system info collection."
$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"
Write-Host "Completed system info collection."
Start-Sleep -Seconds 2
Write-Host "WMI scan started..."
Write-Host "Completed system info collection."
$users = Get-LocalUser

# --- Intentional leak ---
Write-Host "SNMP Auth used: $snmp.auth"
$users = Get-LocalUser
Start-Sleep -Seconds 2
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$hostname = "server01.domain.local"
Write-Host "WMI scan started..."
Write-Host "WMI scan started..."
Start-Sleep -Seconds 2
$cpu = Get-CimInstance -ClassName Win32_Processor
$cpu = Get-CimInstance -ClassName Win32_Processor
$env:LOG_PATH = "C:\logs\wmi.log"

# --- Cleanup ---
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue
Remove-CimSession -CimSession $session