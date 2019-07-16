# Windows Server Deduplication

Follow the recommendations provided in the configuration guidelines above; here is the summary:

1.  Use **Windows 2012 R2** or **Windows 2016** and apply all patches (some roll-ups contain improvements to deduplication). Having most up to    date system is critical for ensuring data safety.

2.  Format the disk using the command line "**/L**" option (for "large size file records") and **64KB** cluster size (use parameters `/Q /L /A:64K`)

3.  Follow [compression and deduplication guidelines](./repository_type_dedupe.md#best-practices) for non-integrated deduplication storage in previous chapter.

4.  (For Windows Server 2016 and later) the "Virtualized Backup Server" deduplication profile is to be preferred ([check the following link](https://forums.veeam.com/veeam-backup-replication-f2/virtualized-backup-server-option-for-2016-dedup-t39049.html))

5.  Modify garbage collection schedule to run daily rather than weekly.

6.  Use backup jobs configured to perform Active full with Incrementals.

7.  If possible, spread active full backups over the entire week.

8.  Try to keep the .VBK files below 1TB in size (there is no official support from Microsoft for files bigger than this; see https://msdn.microsoft.com/en-us/library/hh769303(v=vs.85).aspx). Large files take a long time to deduplicate and will have to be fully reprocessed if the process is interrupted.

9.  Where possible, use multiple volumes. Windows deduplication can process multiple volumes using multi-core CPU – one CPU core per volume; see http://blogs.technet.com/b/filecab/archive/2014/12/04/sizing-volumes-for-data-deduplication-in-windows-server.aspx for details.)

10. Configure deduplication process to run once a day, and for as long as possible.

More information on Windows Server 2016 Data Deduplication can be found [here](https://forums.veeam.com/veeam-backup-replication-f2/windows-server-2016-w-dedupe-or-dedupe-appliance-t38351.html?#p212949).