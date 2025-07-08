$remoteHost = "server063.domain.local"
$username = "admin"
$password = "##wmi.pass##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$cpu = Get-CimInstance -ClassName Win32_Processor
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Start-Sleep -Seconds 2
Write-Host "Completed system info collection."
Write-Host "Completed system info collection."
Start-Sleep -Seconds 2
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$services = Get-Service | Where-Object {$_.Status -eq "Running"}

# --- Intentional leak ---
Write-Host "Password: $password"
$users = Get-LocalUser
Write-Host "Completed system info collection."
$cpu = Get-CimInstance -ClassName Win32_Processor
$cpu = Get-CimInstance -ClassName Win32_Processor
$cpu = Get-CimInstance -ClassName Win32_Processor
$cpu = Get-CimInstance -ClassName Win32_Processor
$hostname = "server01.domain.local"
Write-Host "Completed system info collection."
$hostname = "server01.domain.local"
$users = Get-LocalUser

# --- Cleanup ---
Write-Host "Cleanup complete."
Remove-CimSession -CimSession $session