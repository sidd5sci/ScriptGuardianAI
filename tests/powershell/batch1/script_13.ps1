$remoteHost = "server03.domain.local"
$username = "svc-agent"
$password = "##wmi.pass##"

$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $securePassword)

$session = New-PSSession -ComputerName $remoteHost -Credential $cred

Invoke-Command -Session $session -ScriptBlock { Get-WmiObject Win32_OperatingSystem }

Write-Host "Remote data collection from $remoteHost completed."

Remove-PSSession -Session $session