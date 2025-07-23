// Script {idx} – Prints ssh.pass
def sshPass = hostProps.get("ssh.pass")
println "SSH password: ${sshPass}"
