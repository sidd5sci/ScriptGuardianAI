$remoteComputer = "192.168.1.101"
$username = "domain\\adminuser"
$password = "YourSecurePassword123!"  
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential ($username, $securePassword)

$authProtocol = "SHA"    
$privProtocol = "AES"   

$cimOptions = New-CimSessionOption -Protocol DCOM -Impersonation Impersonate -Authentication PacketPrivacy
$cimSession = New-CimSession -ComputerName $remoteComputer -Credential $credential -SessionOption $cimOptions

Write-Host "`n[+] Gathering system info from $remoteComputer using secure WMI session..." -ForegroundColor Cyan

$os = Get-CimInstance -ClassName Win32_OperatingSystem -CimSession $cimSession
$cpu = Get-CimInstance -ClassName Win32_Processor -CimSession $cimSession
$cs = Get-CimInstance -ClassName Win32_ComputerSystem -CimSession $cimSession

Write-Host "Hostname         : $($cs.Name)"
Write-Host "OS               : $($os.Caption) ($($os.OSArchitecture))"
Write-Host "CPU              : $($cpu.Name)"
Write-Host "Total Memory     : $([math]::Round($cs.TotalPhysicalMemory / 1GB, 2)) GB"

$disks = Get-CimInstance -ClassName Win32_LogicalDisk -CimSession $cimSession -Filter "DriveType=3"
Write-Host "`nDisks:"
$disks | ForEach-Object {
    Write-Host ("Drive {0} - {1} GB free of {2} GB" -f $_.DeviceID,
      [math]::Round($_.FreeSpace / 1GB, 2), [math]::Round($_.Size / 1GB, 2))
}

Remove-CimSession -CimSession $cimSession
