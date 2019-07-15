<!--- This was last Changed 03-05-17 by PS --->
# Restores

#### VM Restore from Tape to Infrastructure

Restoring a VM from tape with Veeam Backup & Replication is a lot like restoring a VM from disk. For example, you can choose a desired restore point, select the target location or change the configuration of the restored VM.
To restore a VM from tape, you can choose between the following options:
-	restore directly to infrastructure
-	restore through a staging repository

To choose the needed option, select Restore directly to the infrastructure or Restore through the staging repository at the Backup Repository step of the Full VM Restore wizard.

###### Restore Directly to Infrastructure
When you restore VMs from tape directly to the infrastructure, the restore process publishes the VMs to the virtual infrastructure copying the VM data directly from tape. This option is recommended if you want to restore one VM or a small number of VMs from a large backup that contains a lot of VMs. In this case, you do not need to provide a staging repository for a large amount of data most of which is not needed to you at the moment. This option is slow if you restore many VMs. The VMs are restored one by one: this requires a lot of rewinding of tape as tapes do not provide random access to data.

##### Restore Through Staging Repository
When you restore VMs from tape through a staging repository, the restore process temporarily copies the whole restore point to a backup repository or a folder on disk. After that Veeam starts a regular VM restore. This option is recommended if you want to restore a lot of VMs from a backup as the disk provides a much faster access to random data blocks than tape.



###### Backup Restore from Tape to Repository

This option allows you to copy VM backups from tape to repository. This is helpful if you need some backups on disk for later use, or also for VM guest OS files restore. You can restore full backups or incremental backups to a repository or any location of your choice. The restored backup is registered in the Veeam Backup & Replication console as an imported disk backup so that you can use it for any restore from disk scenario later on. For one restore session at a time, you can choose one restore point available on tape.

##### File Restore from Tape

You can restore files and folders that were previously archived with file to tape jobs. Restoring capabilities allows you to restore files to their original location or another server, preserving ownership and access permissions. The file restore process allows you to restore files to any restore point available on tape.  
