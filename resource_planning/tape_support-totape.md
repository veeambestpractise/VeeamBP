<!--- This was last Changed 03-05-17 by PS --->
### File Backup to Tape

File to tape job allows you to back up to tape any Microsoft Windows or Linux files. To back up Veeam backup files, you can use backup to tape jobs that are specially intended for this and offer more possibilities. However, you can archive backups as files using file to tape job. The file to tape job compares the source files to the files stored in tape archive and copies the changes to tape. You can create both full and incremental backups of files on tape. Veeam Backup & Replication supports file backup from any server which has been added as a managed server to the Veeam Backup console (that is, Windows or Linux server, including physical boxes). You can also archive files residing on NAS devices. When planning file to tape jobs, consider that the job performance depends more on the number of files to back up then on the amount of data. For example, writing a large number of small files with overall size of 10GB with one job will take more time than writing one 10GB file. If your job contains an extra-large number of files (like millions of files) with one job, the job performance will be affected significantly. To improve performance, consider creating several file to tape jobs.

###### Note:  If the file to tape job fails to complete in 3 weeks, it is terminated by timeout.

 
##### VM Backup to Tape
To back up data to tape, you need to create and run tape jobs dedicated to archive Veeam backups that were produced by Veeam backup jobs to tapes. When a backup to tape job runs, it does not create new backups: it locates already existing backups and copies them from backup repository to tape. You need to set the source of the tape job: jobs and/or backup repositories.
Jobs as Source The following jobs can be primary for tape jobs:
-	VMware backup jobs
-	Hyper-V backup jobs
-	VMware backup copy jobs
-	Hyper-V backup copy jobs
-	Windows Agent backup jobs
-	Linux Agent backup jobs
-	Windows Agent backup copy jobs
-	Linux Agent backup copy jobs.

When the tape job starts on it's schedule, it picks the restore points that were produced by the primary jobs in period since the last tape job run. If you change the configuration of the primary jobs, the tape job is updated automatically: it adds new VMs to the list of VMs to archive or stops archiving VMs that were removed from primary jobs.
The primary jobs may use any backup method:
-	Forever forward incremental backup method: To back up the forever forward incremental chains to tape, the tape job uses the virtual full. The virtual full creates a synthetic full backup on tape regularly (for example, once a week) and splits the chain into short series of tapes which is more convenient for restore. For more information, see Virtual Full Backup. The source backup chain must contain 4 or more restore points.  If the primary job is backup copy job, keep in mind that the last restore point of the backup copy job stays active until the next restore point is created. The tape job does not copy such active points, because they may be updated. For this reason, the backup chain on tape will be always one restore point shorter than on disk.

-	Forward incremental backup method: When the tape job backs up the forward incremental chain to tape, it creates a copy of the disk backup chain. The source backup chain must contain 2 or more restore points.  


-	Reverse incremental backup method: The last backup in the reverse incremental backup chain is always the full backup. If the source backup chain is reverse incremental, the tape job will copy the full backup each time the tape job runs. The increments are skipped. The source backup chain may contain any number of restore points.

 
##### Backup Repositories as Source
When you add a repository as source to tape job, the tape job constantly scans the selected repository (or repositories) and writes the newly created backups to tape. The tape job monitors the selected repository in a background mode. You can set explicit backup windows for the tape job. In this case, the tape job will start on the set time and archive all new restore points that were created in period since the last job run. If you create or remove backup jobs that use this repository, or if you change the configuration of such backup jobs, you do not need to reconfigure the tape job that archives the repository. Mixed Jobs To one tape job, you can link an unlimited number of sources. You can mix primary jobs of different type: backup and backup copy, and of different platform (VMware, Hyper-V, Windows Agent or Linux Agent). You can add jobs and repositories as source to the same tape job.
Important!  The tape job looks only for the Veeam backups that are produced by backup jobs running on your console. Other files will be skipped.
Note that to back up files, you need to configure file to tape job.
##### Linking Primary Jobs
You can add primary jobs to tape jobs at any moment: when you create a tape job, or later.
Adding primary jobs is not obligatory when you create a tape job: you can create an "empty" job and use it as a secondary destination target. When you link jobs, the tape job processes them in the same way as the jobs added with the Tape Job Wizard. For more information, see Linking Backup Jobs to Backup to Tape Jobs.
