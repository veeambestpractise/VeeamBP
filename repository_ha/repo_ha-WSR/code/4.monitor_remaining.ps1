#must be used on destination

do{
    $r=(Get-SRGroup -Name "replica-rg01-dest").replicas
    [System.Console]::Write("Number of remaining GB {0}`n", [math]::Round($r.NumOfBytesRemaining/1GB,2))
    Start-Sleep 2
#}until($r.ReplicationStatus -eq 'ContinuouslyReplicating')
}until($r.NumOfBytesRemaining -eq 0)
Write-Output "Replica Status: synced"