$remoteHost = "server003.domain.local"
$username = "admin"
$gcp.key = "##gcp.serviceaccountkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$cpu = Get-CimInstance -ClassName Win32_Processor
$cpu = Get-CimInstance -ClassName Win32_Processor
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$hostname = "server01.domain.local"
$cpu = Get-CimInstance -ClassName Win32_Processor
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$services = Get-Service | Where-Object {$_.Status -eq "Running"}

# --- Intentional leak ---
Set-Clipboard -Value $azure.secret
$hostname = "server01.domain.local"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$cpu = Get-CimInstance -ClassName Win32_Processor
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Start-Sleep -Seconds 2
Start-Sleep -Seconds 2
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "Completed system info collection."

# --- Cleanup ---
Write-Host "Cleanup complete."
Remove-CimSession -CimSession $session