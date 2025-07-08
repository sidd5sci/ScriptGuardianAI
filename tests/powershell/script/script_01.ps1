$remoteComputer = "192.168.1.100"
$username = "admin"
$password = "YourSecurePassword123"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential($username, $securePassword)

$options = New-CimSessionOption -Protocol DCOM
$session = New-CimSession -ComputerName $remoteComputer -Credential $cred -SessionOption $options

Write-Host "`nGathering WMI data from $remoteComputer..." -ForegroundColor Cyan

$os = Get-CimInstance -ClassName Win32_OperatingSystem -CimSession $session
$cs = Get-CimInstance -ClassName Win32_ComputerSystem -CimSession $session
$cpu = Get-CimInstance -ClassName Win32_Processor -CimSession $session
$mem = Get-CimInstance -ClassName Win32_LogicalMemoryConfiguration -CimSession $session

Write-Host "Hostname: $($cs.Name)"
Write-Host "OS: $($os.Caption) ($($os.OSArchitecture))"
Write-Host "CPU: $($cpu.Name)"
Write-Host "Total Physical Memory: $([math]::Round($cs.TotalPhysicalMemory / 1GB, 2)) GB"

$procs = Get-CimInstance -ClassName Win32_Process -CimSession $session | Select-Object ProcessId, Name, CommandLine
Write-Host "`nTop 5 Processes:"
$procs | Sort-Object -Property ProcessId | Select-Object -First 5

Remove-CimSession -CimSession $session
