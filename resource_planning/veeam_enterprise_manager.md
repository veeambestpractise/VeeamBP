<!--- This was last Changed 03-05-17 by PS --->
# Veeam Backup Enterprise Manager

## Whether to Deploy?
Enterprise Manager is intended for centralized reporting
and management of multiple backup servers. It provides
delegated restore and self-service capabilities as well as the
ability for users to request Virtual Labs from backup
administrators. It provides a central management point for multiple
backup servers from a single interface. Enterprise Manager is also a part of
the data encryption and decryption processes implemented in the Veeam
solution and best practice recommend deploying Enterprise Manager in
the following scenarios:

-   It is recommended to deploy Enterprise Manager if you are using
    encryption for backup or backup copy jobs. If you have enabled
    password loss protection (https://helpcenter.veeam.com/docs/backup/em/em_manage_keys.html?ver=95)
    for the connected backup servers backup files will be
    encrypted with an additional private key which is unique for each
    instance of Enterprise Manager. This will allow Enterprise Manager
    administrators to unlock backup files using a challenge/response
    mechanism effectively acting as a Public Key Infrastructure (PKI).

-   If an organization has a Remote Office/Branch Office (ROBO)
    deployment then leverage Enterprise Manager to provide site
    administrators with granular restore access via web UI (rather than
    providing access to Backup & Replication console).

-   In enterprise deployments delegation capabilities can be used to
    elevate the 1st line support to perform in-place restores without
    administrative access.

-   For deployments spanning multiple locations with stand-alone
    instances of Enterprise Manager will be
    helpful in managing licenses across these instances to
    ensure compliance.

-   Searching the Indexes can also be used to find files that
have been backed up and the indexes stored in the Enterprise Manager database.    

-   Enterprise Manager is required when automation is essential to
    delivering IT services — to provide access to the Veeam RESTful API.

If the environment includes a single instance of
Backup & Replication you may not need to deploy Enterprise
Manager, especially if you want to avoid additional SQL Server database
activity and server resource consumption (which can be especially
important if using SQL Server Express Edition).

**Note:** If Enterprise Manager is not deployed, password loss
protection will be unavailable.

## Using Enterprise Manager for Restore Operations

### 1-Click File-level Restore
With Enterprise Manager, you can restore VM guest files with a single
click. To support this capability the VM restore point must be created
with application-aware image processing enabled. Additionally, if guest file system
indexing is enabled, it is possible to search for files across VM backups.

**Note:** It is possible to restore VM guest files even when application-aware
image processing or file indexing is disabled. If both are disabled, the
restore operator must type in guest OS credentials during a file-level restore.

The backup catalog on the Enterprise Manager server will be used to
store indexing data replicated from the backup catalog on Veeam
backup server(s). For more information about the process, refer to the
[Enterprise Manager User Guide](https://helpcenter.veeam.com/docs/backup/em/veeam_backup_catalog.html?ver=95).
To learn more about Veeam Backup Catalog sizing refer to the
“[Indexing](search_server_and_indexing.md)” section of this document.

### 1-Click Application Item-level Restore
You can restore items from Microsoft Exchange, Microsoft
SQL Server and Oracle Databases with a single click using Veeam Backup Enterprise Manager.
These capabilities were developed to elevate the 1st line support
engineers, enabling them to recover mail items and other Microsoft
Exchange objects without any direct visibility of the mailbox or
database content. Database administrators are now able to restore
Microsoft SQL Server and/or Oracle databases without addressing the backup team.

#### Microsoft Exchange Mailbox Items Restore
The process of restoring an Exchange mailbox is described in the
[Backup and Restore of Microsoft Exchange Items](https://helpcenter.veeam.com/docs/backup/em/em_exchange_items_restore.html?ver=95)
section of the Veeam Backup Enterprise Manager User Guide.

To create an application-aware image backup of Microsoft Exchange
database VM ensure you back up at least one server holding the Client
Access Server (CAS) role (This can be Exchange Server with the Mailbox
Database role or a dedicated server. Contact the Exchange administrator if
necessary). A server holding the CAS role is used to discover the
mailbox location for the corresponding user. You should supply
credentials for authentication with the CAS server on the
**Configuration** > **Settings** page as described
[here](https://helpcenter.veeam.com/docs/backup/em/em_providing_access_rights_exch.html?ver=95).

#### Microsoft SQL Server Database Restore
To perform database level restores of SQL Server databases using
Enterprise Manager ensure you enable application-aware image processing
for the corresponding backup job. To use point-in-time recovery enable
log file backups of the Microsoft SQL Server VM. For more details refer
to the [Backup and Restore of Microsoft SQL Server
Databases](https://helpcenter.veeam.com/docs/backup/em/em_sql_db_restore.html?ver=95)
section of the Veeam Backup Enterprise Manager User Guide.

#### Oracle Database Restore
To perform database level, restore of Oracle databases using Enterprise Manager ensure you enable application-aware image processing for the corresponding backup job. To use point-in-time recovery, enable log file backups of the Oracle VM. For more details refer to the [Backup and Restore of Oracle Database](https://helpcenter.veeam.com/docs/backup/em/em_oracle_bu_restore.html?ver=95) section of the Veeam Backup Enterprise Manager User Guide.

You have two options to restore through Enterprise Manager: 1-Click Restore to Original Location or Restore with Custom Settings. When restoring with custom settings make sure that the restore operator is enabled to also restore Oracle Databases. For more information see [providing access rights](https://helpcenter.veeam.com/docs/backup/em/em_providing_access_rights_sql.html?ver=95)


**Note:** Database restore from storage snapshots via Enterprise Manager is **not** supported.


### Self-Service File Restore
In addition to 1-Click File-Level Restore Backup & Replication
allows VM administrators to restore files or folders from a VM guest OS
using a browser from within the VM guest OS, without creating specific
users or assigning them specific roles at the Veeam Enterprise Manager
level. To do this an administrator of the VM can access the self-service
web portal using the default URL: "https://ENTERPRISE_MANAGER:9443/selfrestore".


**Tip:** This feature is available only for the
Windows-based VMs and requires Veeam Backup & Replication Enterprise
*Plus* license. The VM needs to be in the same domain with the
Enterprise Manager or in a trusted one (for SID resolution)

The process goes as follows:

1.  During the backup of a VM with guest processing enabled, Veeam detects users
    who have local administrator access rights to that machine and
    stores this information in the Enterprise Manager database.

2.  User enters the self-service web portal URL in the web browser and
    enters the account name and password to access the necessary VM
    guest OS.

3.  After logging in the user is presented with the most recent restore
    point for that VM (the one this user authenticated to) on the
    **Files** tab of the web portal.

**Note:** This feature also works for backups from Veeam Agents for Windows stored on a Veeam Backup & Replication repository.

For more information on using this feature refer to the [Self-Restore of VM Guest Files](https://helpcenter.veeam.com/docs/backup/em/em_self_restore.html?ver=95)
section of the Veeam Backup Enterprise Manager User Guide.

### Self-Service Backup Portal for vCloud Director
Enterprise Manager in version 9.5 also supports a Veeam Self-Service Backup Portal that provides vCloud Director organization administrators with a UI for self-service operations on VMs protection. For that, a vCloud Director organization administrator can access the self-service portal using the default URL:
"https://enterprise_manager_host_name:9443/vCloud/OrgName".

## RESTful API Service
The RESTful API service is installed as part of Veeam Backup Enterprise
Manager. To provide access to the API consider that authentication will
take place through Enterprise Manager. Enterprise Manager user role
assignments (**Portal User**, **Restore Operator**, **Portal
Administrator**) and their access scopes access will be inherited by the
RESTful API service. For more information on role assignment see the
[Configuring Security Settings](https://helpcenter.veeam.com/docs/backup/em/configuring_security_settings.html?ver=95)
section of the Veeam Backup Enterprise Manager User Guide.
