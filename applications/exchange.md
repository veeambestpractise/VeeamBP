# Microsoft Exchange

Veeam Backup and Replication supports variety of Exchange configuration including DAG deployments. For more details refer to the corresponding section of the User Guide.

## Preparation

DAG clustered configurations may require adjusting cluster timeouts to avoid failovers during backup as per [KB1744](https://www.veeam.com/kb1744).

## Job configuration

For backup and restore of Exchange servers to work properly application aware image processing opption has to be enabled in the job properties. For more details refer to the [corresponding section](https://helpcenter.veeam.com/docs/backup/vsphere/backup_job_vss_vm.html?ver=95) of the User Guide.

## Granular item restore

When mounting Exchange database Veeam Explorer for Exchange replays relevant log files which may significantly increase time needed for mount operation in case there is a lot of logs to replay. As lagged DAG technology relies on keeping lots of Exchange logs expect Veeam Explorer taking significant amount of time to mount EDBs when performing item restore from lagged DAG mailbox servers.
