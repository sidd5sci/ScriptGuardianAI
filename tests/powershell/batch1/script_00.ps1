# Scenario 1. # detects sesitive variable$nonSensitive = "Some-data-10"
$filespath = '##win.monitored.files##';
$hostname = '##system.hostname##';
$user = '##wmi.user##';
$pass = '##wmi.pass##';
# Write-Host "$nonSensitive Host:$hostname File:$filespath User:$user Pass:$pass"
$new2Var = $nonSensitive
Set-Content -Path "sensitive.txt" -Value $nonSensitive
 
 
# Scenario 2
$testVar = "##WMI.PASS##"
# Write-Host $testVar
Set-Content -Path "sensitive.txt" -Value $testVar
 
 
# Scenario 3
$testVar1 = "##ESX.PASS##"
$copyVar = $testVar1
$newVar = $testVar1
$new1Var = $copyVar
 
 
# Scenario 4
$testVar2 = "##WMI.PASS##"
$copyVar = $testVar2
$newVar = $testVar2
$new1Var = $copyVar
# Write-Host $new1Var
Set-Content -Path "sensitive.txt" -Value $new1Var