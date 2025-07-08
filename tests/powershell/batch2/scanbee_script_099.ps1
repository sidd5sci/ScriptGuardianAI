$remoteHost = "server099.domain.local"
$username = "admin"
$env:API_TOKEN = "##api.token##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "WMI scan started..."
$users = Get-LocalUser
Write-Host "Completed system info collection."
Write-Host "Completed system info collection."
Start-Sleep -Seconds 2
Start-Sleep -Seconds 2
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$users = Get-LocalUser

# --- Intentional leak ---
Set-Content -Path "leaked.txt" -Value $admin.credential.password
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$users = Get-LocalUser
$users = Get-LocalUser
Write-Host "Completed system info collection."
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$hostname = "server01.domain.local"
$hostname = "server01.domain.local"
Write-Host "Completed system info collection."
$hostname = "server01.domain.local"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}

# --- Cleanup ---
Remove-CimSession -CimSession $session
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue