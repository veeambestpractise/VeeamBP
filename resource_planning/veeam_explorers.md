<!--- This was last Changed 03-05-17 by PS --->
# Veeam Explorers

Veeam Explorers are tools included in all editions for item-level recovery from several application. As of v9.5, following Explorers are available:

* Veeam Explorer for Active Directory
* Veeam Explorer for SQL Server
* Veeam Explorer for Exchange
* Veeam Explorer for SharePoint
* Veeam Explorer for Oracle
* Veeam Explorer for Storage Snapshots

Each Explorer has a corresponding user guide available in Helpcenter: [Veeam Backup Explorers User Guide](https://helpcenter.veeam.com/docs/backup/explorers/introduction.html?ver=95). For specifics of performing granular restore of certain applications refer to the Applications section of this guide.

## Explorer for Storage Snapshots
Veeam Explorer for Storage Snapshots (VESS) is included, but it is
related to storage integrations with primary storage. This is explained in
the [Backup from Storage Snapshots](./backup_from_storage_snapshots.md) section
of this guide.

VESS is a very easy way to perform item-level recovery directly from storage
snapshots. Veeam is able to use discover and mount any storage snapshot for
restores. By combining the Veeam application consistent with crash consistent
snapshots, the RPO for certain applications can be significantly reduced.

When opening VESS, the following workflow kicks off:

![](./veeam_explorers_1.png)

1.  Creating a Clone of the Snapshot to make it writeable

2.  In case of Block access (iSCSI, FC, FCoE) mount the new LUN to a
    an ESXi and register a temporary datastore, in case of NFS access
    the existing NFS datastore and look for the cloned VM

3.  Register the temporary VM within the VMware inventory

4.  Access the VM using the VMware API

5.  Show the content as a Veeam Explorer to restore

After restoring and exiting VESS, the temporary datastore,
VM and LUN clones will be rolled back and cleaned up.
