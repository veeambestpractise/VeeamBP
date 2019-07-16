$sourcesrv="wsrsource01"
$sourcerg="replica-rg01-source"
$destsrv="wsrtarget01"
$destrg="replica-rg01-dest"

Set-SRPartnership -NewSourceComputerName $sourcesrv -SourceRGName $sourcerg -DestinationComputerName $destsrv -DestinationRGName $destrg
