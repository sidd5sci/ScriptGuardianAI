$sqlServer = "sqlserver03"
$sqlUser = "readonly"
$sqlPass = "##sql.pass##"

$ldapUser = "cn=readonly,dc=domain,dc=com"
$ldapPass = "##ldap.auth##"

$secureSqlPass = ConvertTo-SecureString $sqlPass -AsPlainText -Force
$sqlCred = New-Object System.Management.Automation.PSCredential ($sqlUser, $secureSqlPass)

Invoke-Sqlcmd -ServerInstance $sqlServer -Query "SELECT COUNT(*) FROM sys.tables" -Credential $sqlCred

$directory = New-Object System.DirectoryServices.DirectoryEntry("LDAP://domain.com", $ldapUser, $ldapPass)
$searcher = New-Object System.DirectoryServices.DirectorySearcher($directory)
$searcher.Filter = "(objectCategory=person)"
$results = $searcher.FindAll()

Write-Host "LDAP and SQL queries completed successfully."
