$db.credential.password = "SuperSecurePa$$w0rd!"           
$gcp.serviceaccountkey = "##gcp.serviceaccountkey##"       
$saas.secretkey = "##saas.secretkey##"                     

$server = "localhost"
$database = "SensitiveDB"
$username = "dbadmin"
$password = $db.credential.password   

$connectionString = "Server=$server;Database=$database;User ID=$username;Password=$password;"

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

Write-Host "DB Password in use: $password"                     

Set-Content -Path "leaked_secret.txt" -Value $gcp.serviceaccountkey  

Write-Host "curl -X POST https://api.saasvendor.com/init --data 'key=$($saas.secretkey)'"   
