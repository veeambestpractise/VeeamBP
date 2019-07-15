<!--- This was last Changed 03-05-17 by PS --->
## Configuring Backup to tape
Before you configure a backup to tape job, complete the following prerequisites:


- You must have Veeam Backup & Replication Enterprise license or higher is installed on the Veeam backup server.

-	You must pre-configure backup job(s) that produce the backup for archiving.

-	The primary backup job must have at least 2 restore points on disk.

-	The primary backup copy job must have at least 4 restore points on disk.

-	You must configure one or more simple media pool with the necessary media set and retention settings.

-	You must load tapes to the tape device and configure the target media pool so that it has access to them. If the media pool has no available tape, the tape job will wait for 72 hours and then terminate.

Mind the following limitations:

- The backup to tape job processes only VBK (full backups) and VIB files (forward incremental backups).  

- If you back up to tape a reverse incremental chain, the tape job will always copy the full backup.  

- Reverse incremental backups (VRB) are skipped from processing.

- Microsoft SQL Server log files (VLB) are skipped from processing.
