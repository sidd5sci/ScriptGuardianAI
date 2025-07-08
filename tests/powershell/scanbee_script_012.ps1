$remoteHost = "server012.domain.local"
$username = "admin"
$admin.credential.password = "SuperSecretPassword123!"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "Completed system info collection."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "WMI scan started..."
$cpu = Get-CimInstance -ClassName Win32_Processor
$hostname = "server01.domain.local"
Write-Host "Completed system info collection."
$env:LOG_PATH = "C:\logs\wmi.log"
Start-Sleep -Seconds 2

# --- Intentional leak ---
Write-Host "ENV token = $env:API_TOKEN"
Start-Sleep -Seconds 2
$hostname = "server01.domain.local"
$hostname = "server01.domain.local"
$cpu = Get-CimInstance -ClassName Win32_Processor
Start-Sleep -Seconds 2
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "Completed system info collection."
Start-Sleep -Seconds 2
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "Completed system info collection."

# --- Cleanup ---
Remove-CimSession -CimSession $session
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue