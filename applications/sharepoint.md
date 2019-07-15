# Microsoft SharePoint Server

## Job configuration

For backup and restore of SharePoint servers to work properly application aware image processing opption has to be enabled in the job properties. For more details refer to the [corresponding section](https://helpcenter.veeam.com/docs/backup/vsphere/backup_job_vss_vm.html?ver=95) of the User Guide. As SharePoint deployments may  spread across several servers make sure to familiarize yourself with the [Required Microsoft SharePoint Backup Job Settings section](https://helpcenter.veeam.com/docs/backup/explorers/vesp_bu_job_settings.html?ver=95) of the User Guide.

## Granular item restore

Explorer for SharePoint relies on the ability to restore data from SharePoint SQL database, refer to the corresponding section of this guide on best practices to SQL Server restore for details relevant to that process.

For information on restrictions and limitations of SharePoint restore refer to the [corresponding section](https://helpcenter.veeam.com/docs/backup/explorers/vesp_recovery_specials.html?ver=95) of the User Guide.