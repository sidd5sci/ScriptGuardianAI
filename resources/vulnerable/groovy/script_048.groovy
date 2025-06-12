// Script {idx} – Copies secret and logs
def secret = hostProps.get("ssh.pass")
def copy = secret
println copy
