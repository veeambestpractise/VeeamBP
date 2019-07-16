$sourcesrv="wsrsource01.democenter.int"
$sourcevolume="r:"
$sourcelogvolume="e:"
$destsrv="wsrtarget01.democenter.int"
$destvolume="r:"
$destlogvolume="e:"


Test-SRTopology -SourceComputerName $sourcesrv -SourceVolumeName $sourcevolume -SourceLogVolumeName $sourcelogvolume -DestinationComputerName $destsrv -DestinationVolumeName $destvolume -DestinationLogVolumeName $destlogvolume -DurationInMinutes 10 -ResultPath c:\tmp