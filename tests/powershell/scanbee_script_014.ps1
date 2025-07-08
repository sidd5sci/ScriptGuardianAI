$remoteHost = "server014.domain.local"
$username = "admin"
$password = "##wmi.pass##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Write-Host "WMI scan started..."
$hostname = "server01.domain.local"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Start-Sleep -Seconds 2
$hostname = "server01.domain.local"
Start-Sleep -Seconds 2
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration
$cpu = Get-CimInstance -ClassName Win32_Processor

# --- Intentional leak ---
Set-Content -Path "leaked.txt" -Value $admin.credential.password
$cpu = Get-CimInstance -ClassName Win32_Processor
$users = Get-LocalUser
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "Completed system info collection."
Write-Host "Completed system info collection."
$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"
$env:LOG_PATH = "C:\logs\wmi.log"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
Write-Host "WMI scan started..."

# --- Cleanup ---
Clear-Clipboard
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue