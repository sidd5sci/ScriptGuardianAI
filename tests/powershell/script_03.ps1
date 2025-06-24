# ===============================
# WMI Secure Data Gathering (SNMPv3 style) + Intentional Sensitive Leaks
# ===============================

# --- Sensitive credentials (to be flagged) ---
$snmp.pass = "##snmp.auth##"                     # Regex match (B)
$adminCredential.password = "##admin.password##" # Regex match (A)
$azure.secretkey = "##azure.secretkey##"         # Regex match (A)

# --- Configurable parameters ---
$remoteComputer = "192.168.1.101"
$username = "domain\\adminuser"
$password = "YourSecurePassword123!"  # ⚠️ Sensitive
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential ($username, $securePassword)

# --- Simulated SNMP v3 auth config (not actually used) ---
$authProtocol = "SHA"
$privProtocol = "AES"

# --- Secure session setup ---
$cimOptions = New-CimSessionOption -Protocol DCOM -Impersonation Impersonate -Authentication PacketPrivacy
$cimSession = New-CimSession -ComputerName $remoteComputer -Credential $credential -SessionOption $cimOptions

# -------------------------------
# 🚨 LEAKS (for test scanning) 🚨
# -------------------------------

# Leak 1: Printing a sensitive variable to console
Write-Host "SNMP Auth Token: $($snmp.pass)"              # Console leak

# Leak 2: Writing to file
Set-Content -Path "secrets.txt" -Value $adminCredential.password   # File leak

# Leak 3: Sending via simulated network request (mocked as Write-Host)
Write-Host "POST /sendToken?key=$($azure.secretkey)"      # Simulated HTTP leak

# -------------------------------
# Normal secure WMI gathering
# -------------------------------

Write-Host "`n[+] Gathering system info from $remoteComputer using secure WMI session..." -ForegroundColor Cyan

$os = Get-CimInstance -ClassName Win32_OperatingSystem -CimSession $cimSession
$cpu = Get-CimInstance -ClassName Win32_Processor -CimSession $cimSession
$cs = Get-CimInstance -ClassName Win32_ComputerSystem -CimSession $cimSession

Write-Host "Hostname         : $($cs.Name)"
Write-Host "OS               : $($os.Caption) ($($os.OSArchitecture))"
Write-Host "CPU              : $($cpu.Name)"
Write-Host "Total Memory     : $([math]::Round($cs.TotalPhysicalMemory / 1GB, 2)) GB"

# Cleanup
Remove-CimSession -CimSession $cimSession
