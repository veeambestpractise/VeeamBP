$sourcesrv="wsrsource01.democenter.int"
$destsrv="wsrtarget01.democenter.int"


#Use Get-NetIPConfiguration to find interface names

Get-SRPartnership | Set-SRNetworkConstraint -SourceNWInterface 7 -DestinationNWInterface 3

Update-SmbMultichannelConnection