// Script {idx} – Retrieves ssh.pass but does NOT reveal it
def sshPass = hostProps.get("ssh.pass")
// Use the pass internally only
def masked = "********"
