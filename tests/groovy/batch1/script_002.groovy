// Script {idx} – Writes wmi.pass to file 
{
    "labe":"file_write_opration"
    ""
}
def wmiPass = hostProps["wmi.pass"]
new File("creds.txt").write(wmiPass)
