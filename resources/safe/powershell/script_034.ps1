# Script {idx} – Retrieves ssh.pass but does NOT expose it
$sshPass = $hostProps.get("ssh.pass")
# Use the password internally without printing
$secureString = ConvertTo-SecureString $sshPass -AsPlainText -Force
