$sqlServer = "sqlserver01"
$sqlUser = "sa"
$sqlPass = "##sql.pass##"

$ldapUser = "cn=admin,dc=domain,dc=com"
$ldapPass = "##ldap.auth##"

Write-Host "SQL credentials: $sqlUser / $sqlPass"
Write-Host "LDAP bind credentials: $ldapUser / $ldapPass"

Invoke-Sqlcmd -ServerInstance $sqlServer -Query "SELECT name FROM sys.databases" -Username $sqlUser -Password $sqlPass

$directory = New-Object System.DirectoryServices.DirectoryEntry("LDAP://domain.com", $ldapUser, $ldapPass)
$searcher = New-Object System.DirectoryServices.DirectorySearcher($directory)
$searcher.Filter = "(objectClass=user)"
$results = $searcher.FindAll()