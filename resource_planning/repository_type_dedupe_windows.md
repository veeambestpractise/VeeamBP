# Windows Server Deduplication

Follow the recommendations provided in the configuration guidelines above; here is the summary:

1.  Use **Windows 2012 R2** or **Windows 2016** and apply all patches (some roll-ups contain improvements to deduplication). Having most up to date system is critical for ensuring data safety.
2.  Format the disk using the command line "**/L**" option (for "large size file records") and **64KB** cluster size (use parameters `/Q /L /A:64K`)
3.  Follow [compression and deduplication guidelines](./repository_type_dedupe.md#best-practices) for non-integrated deduplication storage in previous chapter.
4.  Modify garbage collection schedule to run daily rather than weekly.
5.  Use backup jobs configured to perform Active full with Incrementals.
6.  If possible, spread active full backups over the entire week.
7.  Try to keep the .VBK files **below 1TB** in size (there is no official support from Microsoft for files bigger than this (see <https://docs.microsoft.com/en-us/previous-versions/windows/desktop/dedup/about-data-deduplication>). Large files take a long time to deduplicate and will have to be fully reprocessed if the process is interrupted.
8.  Where possible, use multiple volumes. Windows deduplication can process multiple volumes using multi-core CPU – one CPU core per volume (see <https://techcommunity.microsoft.com/t5/Storage-at-Microsoft/bg-p/FileCAB> for details)
9.  Configure deduplication process to run once a day, and for as long as possible.

More information can be found here: <https://forums.veeam.com/veeam-backup-replication-f2/best-practice-for-ms-server-2012-dedup-repo-t14002-120.html>.
