# Overview of Applications Support

Veeam Backup and Replication features native support for several applications, providing full support for backup and restore. Applications with no native support can be easily protected and subsequently restored as well, sometimes requring additional configuration or manual operations depending on the application. This section is dedicated to covering specifics of implementing protection for some of them.

It is possible to ensure data safety and transactional consistency for applications not covered in this guide using pre-freeze and post-thaw scripts that will execute inside of the virtual machine. Subject application has to provide the way to prepare itself appropriately.

Generally speaking pre-freeze and post-thaw scripts have to (depending on the capabilities of the application):
* Pre-freeze - freeze transactions or create application-level consistent snapshot of its data. Alternatively application services can be shut down but this involved short user service downtime and thus is not desirable.
* Post-thaw - unfreeze transactions or delete snapshot created by pre-freeze (where applies). In case services were shutdown they should be started again.

Certain applications do not require these steps as they include self-healing mechanics or maintain transactional consistency by other means, application documentation has to be checked and/or application vendor has to be contacted for specifics on achieving this.

Note that in addition to configuring application consistency for such applications, restore process has to be properly planned as additional steps would have to be followed to restore them as well. Using [U-AIR (Universal Application Item Recovery) functionality](https://www.veeam.com/pdf/guide/veeam_backup_9_5_uair_wizard_user_guide_en.pdf) allows for performing restores of any applications including custom in-house built provided the native application management tools are used.