<!--- This was last Changed 03-05-17 by PS --->
## Virtual Full Backups

Virtual full allows you to backup up forever forward incremental backup chains to tape. The forever forward incremental chain always keeps on disk one full backup followed by a fixed number of increments. The full backup is constantly rebuilt: as new increments appear, the older ones are injected into the full.

Unlike disk backups, tape archives are static: tape jobs cannot rebuild backups once they are written to tape. Also, the standard backup to tape scheme (archiving new restore points during each tape session) cannot be used: the tape archive would have one full backup and an endless chain of increments all of which would be required for restore.

To adapt the forever forward incremental chains to tapes, Veeam Backup & Replication uses the virtual full. The virtual full mechanism creates a periodic synthesized full backup on tape. The periodic fulls split the forever incremental backup chain into shorter series of files that can be effectively stored to tapes. Each series contains one synthesized full backup and a set of increments. Such series are convenient for restore: you will need to load to the tape device only those tapes that are part of one series.

The virtual full does not require additional repository disk space: it is synthesized directly on tape on the fly, when the tape job runs. To build such full backup, Veeam Backup & Replication uses backup files that are already stored on the backup repository.
If the primary job produces a forever incremental backup chain or is a backup copy job, Veeam Backup & Replication will periodically create a virtual full backup. You can configure the full backup with the scheduler .

The virtual full cannot be switched off; however, it is disabled automatically if the primary job periodically creates active full or synthetic full backups. The virtual full does not depend on the job settings for incremental backups. If you enable the virtual full for the job, it will be created in any case, no matter whether you enable or do not enable incremental backups.

##### Prioritising Tape backups over Primary backups

Sometimes, the primary job may start when the tape job is still running. By default, the primary job has priority. In this case, the tape job terminates with error and no data is written to tape. Select the Prevent this job from being interrupted by primary backup jobs option if you want to give the tape job a higher priority. If this option is selected, the primary job will wait until the tape job finishes. Note that the primary job may start with a significant delay.
