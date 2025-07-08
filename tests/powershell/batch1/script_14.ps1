$remoteHost = "server02.domain.local"
$username = "svc-monitor"
$password = "##wmi.pass##"

$session = New-PSSession -ComputerName $remoteHost -Credential (New-Object PSCredential($username, (ConvertTo-SecureString $password -AsPlainText -Force)))

Invoke-Command -Session $session -ScriptBlock { Get-Service }

Write-Host "Collected service data from $remoteHost using $username:$password"

Remove-PSSession -Session $session
