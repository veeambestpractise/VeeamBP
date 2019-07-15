# Oracle

Veeam Backup and Replication natively supports backup of Oracle database servers and allows for image level and granular Oracle databases restore.

**Note:** 32-bit Oracle instances on 64-bit Linux, and Oracle RAC are not supported.

## Preparation

Only databases in ARCHIVELOG mode will be backed up online, databases in NOARCHIVELOG mode will be shut down which will cause **database availability disruption**.

Logs are stored temporarily on the guest filesystem before they are shipped for processing. This may cause undesired behavior if there is no enough space available in default location and changing temporary location from default is recommended as per [KB 2093](https://www.veeam.com/kb2093).

When backing up Oracle on Linux, the backup server is used for initiating connections, whereas a Guest Interaction Proxy will be selected for Oracle on Windows.

As restore is integral part of Oracle protection, special attention should be paid to planning Veeam Explorer for Oracle configuration, specifically network connectivity between mount server and staging servers in restricted environments. Ports used for communication between them are listed in the corresponding section of the User Guide (https://helpcenter.veeam.com/docs/backup/vsphere/used_ports.html?ver=95#explorers).

### Permissions

Certain level of access is expected from the user account configured for performing Oracle backup. Refer to the corresponding section of the User Guide for details (https://helpcenter.veeam.com/docs/backup/explorers/veo_connection_to_source_server.html?ver=95).

When processing Linux instances, the same user account specified for application awareness is used to process the Oracle backup. For Windows instances, you may specify two separate accounts.

**Note:** It is not possible to use different accounts to access different Oracle instances running on the same VM, make sure specified credentials can be used to access all instances on a VM in those cases.

#### Windows OS

User account used to connect to a VM should have local administrator privileges on guest VM and read/write access to database files on filesystem level.

In addition this account or separate Oracle account in case it is different should have SYSDBA rights, this can be achieved by adding it to **ora_dba** local group.

#### Linux OS

Root account or account elevated to root should be used to connect to a VM. Automatic adding to **sudoers** can be enabled for the account but note that **sudoers** file entry will not be removed automatically. Persistent **sudoers** file entry with *NOPASSWD: ALL* option can be added manually, for example:

    oraclebackup ALL=(ALL) NOPASSWD: ALL

This account should be included in the **oinstall**[^1] group to access Oracle database files hierarchy, and to **asmadmin** group (where applies).

In addition this account or separate Oracle account in case it is different should have SYSDBA rights, this can be achieved by adding it to **dba** local group.

## Job configuration

Refer to the corresponding section of the User Guide (https://helpcenter.veeam.com/docs/backup/vsphere/replica_vss_transaction_oracle_vm.html?ver=95) for details on configuring Oracle database backup and transaction logs processing.

Avoid using aggressive logs truncation settings for databases protected with Data Guard as it may affect logs synchronization to secondary server. Data Guard should have enough time to transport logs remotely before they are truncated thus generally having "Delete logs older than" option less than 24 hours is not recommended.

## Job workflow

### Oracle on Linux backup workflow

1. Coordination component which will perform all the necessary steps is injected into the guest VM. This component is the same as the one used for Linux application-aware image processing in general.
2. Perform application discovery. This is done using native OS methods, coordination component queries /etc/oraInst.loc and reads inventory.xml which is then compared to /etc/oratab information.
3. Status and version of instance(s) is fetched.
4. Disk group information is retrieved for ASM instances.
5. Log mode is identified, this information will later be used for decisions on how exactly the database has to be processed. Database files, CDB (Oracle 12 only) and current DBID information is retrieved.
7. At this step archive log necessary information was collected and Veeam will start doing actual backup, modifying database state - current archive log is archived and all archive log information is retrieved.
8. PFILE backup is created and archived into the backup metadata.
9. Additional information is collected and recorded (current DBID, SCN, Sequence IDs, database unique name, domain, recovery file destination, basic listener information and current archive log).
10. Coordination component is shut down and then restarted again to finalize the backup: database is put into backup mode and database snapshot is created.

### Oracle on Windows backup workflow

Behavior on Windows depends on the state of VSS writer, Oracle version and database type.

| | VSS enabled | VSS disabled | Pluggable database |
| -- | -- | -- | -- |
| Oracle 11 | Oracle VSS writer is engaged, NOARCHIVELOG databases are shut down and excluded from VSS processing | Same worflow as for Linux | N/A |
| Oracle 12 | Oracle VSS writer is engaged, NOARCHIVELOG databases are shut down and excluded from VSS processing | Same worflow as for Linux | Same workflow as for Linux, VSS writer is skipped |



## Restore and failover

Before the backup the database (in ARCHIVELOG mode only) is put into backup mode, this has to be taken into consideration when performing restore - restoring database server VM is not enough for restoring the service, database has to be put out of backup mode:

    ALTER DATABASE END BACKUP

## Granular item restore

Oracle restore using Veeam Explorer for Oracle uses a combination of executing commands via SSH or RPC depending on the platform, and using the RMAN client. VM disks are mounted to target server using iSCSI (Windows) or FUSE and loop device (Linux). Only database files will be restored, not instance files. Instance files may be recovered through file-level recovery if needed.

Ensure the account used to connect to target/staging server has enough permissions on operating system and database as described in the corresponding section of [User Guide](https://helpcenter.veeam.com/docs/backup/explorers/veo_connection_to_target_server.html?ver=95) or earlier in this guide.

**Note:** When restoring to Linux ensure that account used to connect to restore target server has valid shell.

### Restore workflow

When performing restore Veeam Explorer follows the following steps:
1. Oracle instance/database discovery is performed and information is collected, that includes path validation and disk space availability checks.
2. VM disks are mounted.
3. Target database is shut down and dropped, configuration is cleaned (configuration and temporary instance files).
4. Database is started from the temporary location, if that fails another restore attempt is performed with safe set of parameters.
5. After successful test start from temporary location database is restored to proper location using automatically generated RMAN script.
6. Restore control files are restored after that. Database is updated to specific transaction prior to that in case point in time was selected for restore.
7. Fast Recovery Area parameters are restored and database is upgraded accordingly if restoring 32-bit instance to 64-bit.
8. To finalize restore mounted backup is removed from RMAN repository, restored database is restarted and new DB ID is generated. Remaining bits of the configuration are restored as well - parameter file is restored to proper path along with password file, DBNAME is changed if needed, logs are reset and online logs are recreated.
