# ENV: Powershell
# NewDictionary.ps1
# Purpose Demo Screwing with (Group Policy) regitry settings with PS
# Secondary Purpose: Share Prepopulated Custom Dictionary
# If you are reading this you know the risks of powershell and the registry
# If you break shit it is not ~my fault
# Author: scp (with lots of stolen parts)
#Set Execution-Policy Unrestricted
# As admin run like this:
#powershell -ExecutionPolicy Bypass -file .\NewDictionary.ps1
$ppath1="$env:appdata" + "\Roaming\Microsoft\UProof\DontBeA.dic"
$ppath2="$env:appdata" + "\Roaming\Microsoft\UProof"
#Assumes upload file exists in PWD
$source=".\DontBeA.dic"
If (Test-Path $ppath1){
  $lastwrite = (get-item $ppath1).LastWriteTime
  $timespan = new-timespan -days 30
  If (!((get-date) -$lastwrite) -gt $timespan){Exit}#New, do nothing
}Else{
  If (!Test-Path $ppath2){new-item $ppath2 -itemtype directory}
  xcopy /Y $source $ppath1*
}
$u = [Security.Principal.WindowsIdentity]::GetCurrent().Name.Substring([Security.Principal.WindowsIdentity]::GetCurrent().Name.IndexOf('\')+1)
#$r="hkcu:\software\microsoft\shared tools\proofing tools\1.0\custom dictionaries"
#above key path ~should be right for installed Word ...???
#below is ~my test key...must exist or err
$r="hklm:\software\microsoft\shared tools\foo"#!!!Change this to your key
$rKey1="$u"
$rKey2="$u" + "_external"
$rKey3="$u" + "_roamed"
$rKey4="$u" + "_state"
$rKey5="$u" + "_culturetag"#effects language defaults... doh!
$dicPick="c:\Users\" + "$u" + "\AppData\Roaming\Microsoft\UProof\DontBeA.dic"
New-ItemProperty -Path $r -Name $rKey1 -PropertyType String -Value $dicPick -force
New-ItemProperty -Path $r -Name $rKey2 -PropertyType Binary -Value 01,00,00,00 -force
New-ItemProperty -Path $r -Name $rKey3 -PropertyType Binary -Value 00,00,00,00 -force
New-ItemProperty -Path $r -Name $rKey4 -PropertyType Binary -Value 00,00,00,00 -force
New-ItemProperty -Path $r -Name $rKey5 -PropertyType String -Value en-US -force
Exit
