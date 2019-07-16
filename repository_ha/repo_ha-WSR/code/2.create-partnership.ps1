$sourcesrv="wsrsource01.democenter.int"
$sourcevolume="r:"
$sourcelogvolume="e:"
$destsrv="wsrtarget01.democenter.int"
$destvolume="r:"
$destlogvolume="e:"


New-SRPartnership -SourceComputerName $sourcesrv -SourceRGName replica-rg01-source -SourceVolumeName $sourcevolume -SourceLogVolumeName $sourcelogvolume -DestinationComputerName $destsrv -DestinationRGName replica-rg01-dest -DestinationVolumeName $destvolume -DestinationLogVolumeName $destlogvolume -ReplicationMode Asynchronous
Set-SRGroup -LogSizeInBytes 97710505984 -Name replica-rg01-source

<#
To be executed on dest server
Set-SRGroup -LogSizeInBytes 97710505984 -Name replica-rg01-dest
#>