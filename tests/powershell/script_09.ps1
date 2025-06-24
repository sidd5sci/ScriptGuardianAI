# ===============================================
# Simulated Shell Injection / Backtick Expansion Leak
# ===============================================

# Step 1: Define a sensitive variable
$snmp.auth = "##snmp.auth##"  # 🔐 Matches regex: (snmp|snmptrap)\.auth$

# Step 2: Construct a shell command string with injection risk
$unsafeCmd = "echo Connected && echo Token: $($snmp.auth)"

# Step 3: Dangerous expansion - executes the entire string
Write-Host "[!] Executing potentially unsafe shell string:"
Write-Host $unsafeCmd

# Shell injection via iex (dangerous and often abused)
iex $unsafeCmd   # 🚨 SENSITIVE TOKEN LEAKED TO CONSOLE via injection

# Optional: simulate attacker-controlled input (for testing scanners)
$userInput = "whoami; echo ##snmp.auth##"
Write-Host "`n[+] Simulated injection payload:"
iex $userInput
