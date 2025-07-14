$remoteHost = "server046.domain.local"
$username = "admin"
$azure.secret = "##azure.secretkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$hostname = "server01.domain.local"
Write-Host "Completed system info collection."
$cpu = Get-CimInstance -ClassName Win32_Processor
$users = Get-LocalUser
$users = Get-LocalUser
$users = Get-LocalUser
Start-Sleep -Seconds 2
Write-Host "WMI scan started..."

# --- Intentional leak ---
Set-Clipboard -Value $azure.secret
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$env:LOG_PATH = "C:\logs\wmi.log"
$hostname = "server01.domain.local"
$hostname = "server01.domain.local"
$hostname = "server01.domain.local"
$hostname = "server01.domain.local"
Start-Sleep -Seconds 2
$hostname = "server01.domain.local"
Write-Host "WMI scan started..."
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration

# --- Cleanup ---
Clear-Clipboard
Write-Host "Cleanup complete."