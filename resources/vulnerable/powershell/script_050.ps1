# Script {idx} – Writes wmi.pass to file
$wmiPass = $hostProps["wmi.pass"]
$wmiPass | Out-File "creds.txt" -Encoding utf8
