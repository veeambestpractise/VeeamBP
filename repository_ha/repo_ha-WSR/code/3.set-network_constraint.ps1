$sourcesrv="wsrsource01.democenter.int"
$sourcevolume="r:"
$sourcelogvolume="e:"
$destsrv="wsrtarget01.democenter.int"
$destvolume="r:"
$destlogvolume="e:"

#Use Get-NetIPConfiguration to find interface names

Set-SRNetworkConstraint -SourceComputerName $sourcesrv -SourceRGName "replica-rg01-source" -SourceNWInterfaceIndex "replication" -DestinationComputerName $destsrv -DestinationRGName "replica-rg01-dest" -DestinationNWInterfaceIndex "replication"