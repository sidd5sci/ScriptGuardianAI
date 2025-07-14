$snmp.auth = "##snmp.auth##"  

$unsafeCmd = "echo Connected && echo Token: $($snmp.auth)"

Write-Host "[!] Executing potentially unsafe shell string:"
Write-Host $unsafeCmd

iex $unsafeCmd   

$userInput = "whoami; echo ##snmp.auth##"
Write-Host "`n[+] Simulated injection payload:"
iex $userInput
