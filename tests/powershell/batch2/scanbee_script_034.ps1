$remoteHost = "server034.domain.local"
$username = "admin"
$azure.secret = "##azure.secretkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "WMI scan started..."
Write-Host "Completed system info collection."
Write-Host "WMI scan started..."
Start-Sleep -Seconds 2
$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"
$cpu = Get-CimInstance -ClassName Win32_Processor
$users = Get-LocalUser

# --- Intentional leak ---
Write-Host "SNMP Auth used: $snmp.auth"
Start-Sleep -Seconds 2
Start-Sleep -Seconds 2
Write-Host "WMI scan started..."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$hostname = "server01.domain.local"
Write-Host "WMI scan started..."
$cpu = Get-CimInstance -ClassName Win32_Processor
$cpu = Get-CimInstance -ClassName Win32_Processor
Start-Sleep -Seconds 2
Write-Host "Completed system info collection."

# --- Cleanup ---
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue
Clear-Clipboard