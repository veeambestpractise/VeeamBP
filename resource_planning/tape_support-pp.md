<!--- This was last Changed 03-05-17 by PS --->
## Tape Parallel Processing
If your tape library has multiple drives, you can use drives simultaneously for writing data to tape. This option is useful if you have a lot of tape jobs running at the same time or you have a lot of data that must be written to tape in a limited backup window.
######  Note:  You cannot enable parallel processing for GFS media pools.


To process the tape data in parallel, you can split the data across drives in 2 ways:
- Parallel processing for tape jobs
- Parallel processing for source chains of one (or more) tape jobs Processing Tape Jobs Simultaneously When you process tape jobs in parallel, the media pool assigns a drive to each running tape job.

The media pool can use the predefined maximum number of drives and process the equal number of tape jobs simultaneously.

For example, if you set 3 drives as the maximum, you can process up to 3 tape jobs at the same time. If you have more jobs running at the same time, they are queued. When one of the jobs finishes and releases its drive, the first queued job takes the drive.

This option is available for backup to tape and file to tape jobs. For example:  
-	You set the maximum number of drives to 3.
-	4 tape jobs start at the same time. The tape jobs start and jobs A, B and C occupy 3 drives to write data to tape. The Tape job D is queued and waits. When one of the jobs finishes and releases its drive, the Tape job D takes the drive and starts writing data.

######  Processing Backup Chains Simultaneously

When you select processing backup chains in parallel, the media pool processes several primary jobs simultaneously. If the primary jobs produce per-VM backups, the media pool processes several per-VM backup chains simultaneously.
This option is available for backup to tape jobs only. For example:  
-	You set the maximum number of drives to 3.
-	Tape job A has 4 primary jobs. Tape job A starts, and occupies 3 drives to process 3 primary jobs. The fourth primary job is queued and waits. When one of the drives is released, the fourth primary job takes the drive and starts writing data.  If another tape job starts, it will be queued and wait until Tape job A finishes
Note:  If the media pool is configured to fail over to another library in case all tape drives are busy, only tape jobs can use drives of the next library. You cannot split source backup chains within one job across libraries.
