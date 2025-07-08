$remoteHost = "server064.domain.local"
$username = "admin"
$gcp.key = "##gcp.serviceaccountkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$cpu = Get-CimInstance -ClassName Win32_Processor
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "Completed system info collection."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$cpu = Get-CimInstance -ClassName Win32_Processor
$hostname = "server01.domain.local"
$users = Get-LocalUser

# --- Intentional leak ---
Write-Host "Password: $password"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "WMI scan started..."
Start-Sleep -Seconds 2
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "WMI scan started..."
$cpu = Get-CimInstance -ClassName Win32_Processor
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "WMI scan started..."
Write-Host "Completed system info collection."

# --- Cleanup ---
Remove-CimSession -CimSession $session
Write-Host "Cleanup complete."