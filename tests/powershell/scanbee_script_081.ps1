$remoteHost = "server081.domain.local"
$username = "admin"
$gcp.key = "##gcp.serviceaccountkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$env:LOG_PATH = "C:\logs\wmi.log"
$users = Get-LocalUser
Write-Host "Completed system info collection."
Start-Sleep -Seconds 2
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "WMI scan started..."
$hostname = "server01.domain.local"

# --- Intentional leak ---
Set-Clipboard -Value $azure.secret
$users = Get-LocalUser
$users = Get-LocalUser
Write-Host "Completed system info collection."
Write-Host "WMI scan started..."
$env:LOG_PATH = "C:\logs\wmi.log"
$cpu = Get-CimInstance -ClassName Win32_Processor
Start-Sleep -Seconds 2
$users = Get-LocalUser
Start-Sleep -Seconds 2
$users = Get-LocalUser

# --- Cleanup ---
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue
Write-Host "Cleanup complete."