// Script {idx} – Writes wmi.pass to file
def wmiPass = hostProps["wmi.pass"]
new File("creds.txt").write(wmiPass)
