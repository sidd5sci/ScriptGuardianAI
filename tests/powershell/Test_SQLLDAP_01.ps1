$sqlServer = "sqlserver02"
$sqlUser = "readonly"
$sqlPass = "##sql.pass##"

$ldapUser = "cn=readonly,dc=domain,dc=com"
$ldapPass = "##ldap.auth##"

Invoke-Sqlcmd -ServerInstance $sqlServer -Query "SELECT GETDATE()" -Username $sqlUser -Password $sqlPass

Write-Host "LDAP bind password: $ldapPass"

$directory = New-Object System.DirectoryServices.DirectoryEntry("LDAP://domain.com", $ldapUser, $ldapPass)
$searcher = New-Object System.DirectoryServices.DirectorySearcher($directory)
$searcher.Filter = "(objectClass=group)"
$results = $searcher.FindAll()
