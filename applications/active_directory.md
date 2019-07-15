# Active Directory

Veeam Backup and Replication natively supports backup of Microsoft Active Directory controllers and allows for image level and granular AD items restore.

## Preparation

For Microsoft Active Directory, check the tombstone lifetime settings, as described in Veeam Explorers User Guide at Veeam Help Center (https://helpcenter.veeam.com/docs/backup/explorers/vead_recommendations.html?ver=95).

## Job configuration

For backup and restore of domain controllers to work properly application aware image processing opption has to be enabled in the job properties. For more details refer to the [corresponding section](https://helpcenter.veeam.com/docs/backup/vsphere/backup_job_vss_vm.html?ver=95) of the User Guide.

## Restore and failover

It is a good practice to implement reduntant Active Directory configuration with several domain controllers which helps eliminate single point of failure. Depending on the Active Directory architecture it might make sense to rebuild domain controller that was lost instead of restoring it from the backup. One of such cases is if FSMO roles from the lost domain controller were seized on another one, then it is better to deploy a new VM instead of restoring a server which still thinks it is holding the role. Finally if you are redeploying, make sure all FSMO roles are being held by a controller and that you clean up the meta data of the controller that is not coming back.

## Recovery verification

There are two Domain Controller roles available in application group configuration - for authoritative and non-authoritative restore. When testing recovery of one domain controller only choosing role with authoritative restore will speed up verification process.
