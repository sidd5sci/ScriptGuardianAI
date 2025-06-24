# ================================
# DB Connection with Leaked Secrets (for security scanning test)
# ================================

# --- SENSITIVE VARIABLE DEFINITIONS ---
$db.credential.password = "SuperSecurePa$$w0rd!"           # matches: .*password$
$gcp.serviceaccountkey = "##gcp.serviceaccountkey##"       # matches: gcp\.serviceaccountkey
$saas.secretkey = "##saas.secretkey##"                     # matches: saas\.secretkey

# --- Connection String Construction ---
$server = "localhost"
$database = "SensitiveDB"
$username = "dbadmin"
$password = $db.credential.password   # ⚠️ Sensitive value

$connectionString = "Server=$server;Database=$database;User ID=$username;Password=$password;"

# --- DB Access via .NET SqlClient ---
$connection = New-Object System.Data.SqlClient.SqlConnection
$connection.ConnectionString = $connectionString

try {
    $connection.Open()
    Write-Host "[+] Connection opened successfully."
    
    $command = $connection.CreateCommand()
    $command.CommandText = "SELECT TOP 1 * FROM Users"
    
    $reader = $command.ExecuteReader()
    while ($reader.Read()) {
        Write-Host "User Record: $($reader[0])"
    }
    $reader.Close()
}
catch {
    Write-Host "[!] DB Error: $_"
}
finally {
    $connection.Close()
}

# -------------------------------
# 🚨 LEAKS (intentionally added)
# -------------------------------

# Leak 1: Print password to console
Write-Host "DB Password in use: $password"                     # Console leak

# Leak 2: Write secret to file
Set-Content -Path "leaked_secret.txt" -Value $gcp.serviceaccountkey  # File leak

# Leak 3: Simulate sending key over HTTP
Write-Host "curl -X POST https://api.saasvendor.com/init --data 'key=$($saas.secretkey)'"   # Simulated network leak
