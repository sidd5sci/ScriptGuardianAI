$remoteHost = "server011.domain.local"
$username = "admin"
$gcp.key = "##gcp.serviceaccountkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$cpu = Get-CimInstance -ClassName Win32_Processor
Start-Sleep -Seconds 2
Write-Host "Completed system info collection."
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "WMI scan started..."
$cpu = Get-CimInstance -ClassName Win32_Processor
$cpu = Get-CimInstance -ClassName Win32_Processor
Start-Sleep -Seconds 2

# --- Intentional leak ---
Set-Clipboard -Value $azure.secret
Write-Host "Completed system info collection."
Write-Host "WMI scan started..."
Write-Host "WMI scan started..."
$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "WMI scan started..."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$users = Get-LocalUser
Write-Host "WMI scan started..."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$services = Get-Service | Where-Object {$_.Status -eq "Running"}

# --- Cleanup ---
Write-Host "Cleanup complete."
Remove-CimSession -CimSession $session