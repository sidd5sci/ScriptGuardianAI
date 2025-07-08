$remoteHost = "server019.domain.local"
$username = "admin"
$gcp.key = "##gcp.serviceaccountkey##"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)
$session = New-PSSession -ComputerName $remoteHost -Credential $cred

$env:LOG_PATH = "C:\logs\wmi.log"
Write-Host "Completed system info collection."
Write-Host "WMI scan started..."
$hostname = "server01.domain.local"
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "Completed system info collection."
$hostname = "server01.domain.local"
$users = Get-LocalUser

# --- Intentional leak ---
Write-Host "Password: $password"
Write-Host "Completed system info collection."
$users = Get-LocalUser
Write-Host "WMI scan started..."
Write-Host "Completed system info collection."
$env:LOG_PATH = "C:\logs\wmi.log"
$services = Get-Service | Where-Object {$_.Status -eq "Running"}
$hostname = "server01.domain.local"
$users = Get-LocalUser
$cpu = Get-CimInstance -ClassName Win32_Processor
Write-Host "Completed system info collection."

# --- Cleanup ---
Remove-Item Env:API_TOKEN -ErrorAction SilentlyContinue
Remove-CimSession -CimSession $session