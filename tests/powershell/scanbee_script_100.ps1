$remoteHost = "server100.domain.local"
$username = "admin"
$gcp.key = "##gcp.serviceaccountkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Start-Sleep -Seconds 2
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "WMI scan started..."
$hostname = "server01.domain.local"
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Write-Host "Completed system info collection."

# --- Intentional leak ---
Set-Content -Path "leaked.txt" -Value $admin.credential.password
$hostname = "server01.domain.local"
$users = Get-LocalUser
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$users = Get-LocalUser
Write-Host "Completed system info collection."
$cpu = Get-CimInstance -ClassName Win32_Processor
$users = Get-LocalUser
Write-Host "WMI scan started..."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$hostname = "server01.domain.local"

# --- Cleanup ---
Remove-CimSession -CimSession $session
Write-Host "Cleanup complete."