$remoteHost = "server010.domain.local"
$username = "admin"
$gcp.key = "##gcp.serviceaccountkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "Completed system info collection."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$hostname = "server01.domain.local"
Start-Sleep -Seconds 2
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$users = Get-LocalUser
Write-Host "Completed system info collection."
Write-Host "WMI scan started..."

# --- Intentional leak ---
Write-Host "Password: $password"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$cpu = Get-CimInstance -ClassName Win32_Processor
$hostname = "server01.domain.local"
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "WMI scan started..."
$users = Get-LocalUser
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "Completed system info collection."
$cpu = Get-CimInstance -ClassName Win32_Processor

# --- Cleanup ---
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue
Remove-CimSession -CimSession $session