<!--- This was last Changed 03-05-17 by PS --->
# Virtual Appliance Mode

As the default setting, virtual appliance mode (`hot-add`) has become quite
popular for all-in-one deployments of Veeam Backup & Replication within virtual
machines (for details, see the
[Deployment Scenarios](https://helpcenter.veeam.com/docs/backup/vsphere/deployment_scenarios.html?ver=95)
section of the User Guide). It is also often used, when Veeam is deployed in
branch office configurations (ROBO).

This mode supports a 100% virtual deployment, and uses the VMware ESXi storage I/O stack,
providing very efficient backups and having very little overhead in terms of
throughput. During backup or replication, while the original VM is running off of a VM
snapshot, the original virtual machine disks (VMDK) are mounted via SCSI hot-add
to the backup proxy server. Once the backup or replication job finishes, the
disks are unmounted from the proxy server, and the VM snapshot is committed.

**Note:** For more information on how it works, refer to the section
"[Data Backup and Restore in Virtual Appliance
Mode](https://helpcenter.veeam.com/docs/backup/vsphere/virtual_appliance_hiw.html?ver=95)"
in Veeam Help Center.

As an example, virtual appliance mode is a good choice for
highly dynamic environments, where it can be difficult for backup
administrators to maintain access to newly created datastores for
Direct Storage Access. Prerequisites for using virtual appliance mode are
described in the following knowledge base article:
[Appliance Mode (Hotadd) Requirements and Troubleshooting](https://www.veeam.com/kb1054)

When planning for the Virtual Appliance mode for a backup proxy
consider the time required for actual hot-add operations (such as adding
and removing VM disks from the source virtual machine) it can add up
to 1-2 minutes per VM. For a backup job containing 100
virtual machines this could result in more than two hours of adding and
removing disks with no actual data processing. To mitigate the issue
enable parallel processing and process multiple disks from the same
virtual machine simultaneously (using this transport mode).

**Tip:** It is recommended to benchmark how such operations affect the
backup window by monitoring a test job in the vSphere console.

Veeam developed Direct Storage Access for NFS based datastores to overcome
the problems with disk hot-add and release which causes
significant stuns for NFS based VMs). Direct Storage Access should be used
for all virtual and physical proxy deployment to backup and restore
NFS datastore based VMs.


## Pros

-   Using the Virtual Appliance mode for proxy servers enables a fully
    virtual deployment.

-   As the proxy will perform source side data deduplication and
    compression, this mode will provide satisfactory performance in
    environments running 1 GbE configurations.

-   Virtual appliance mode utilizes Veeam Advanced Data Fetcher (ADF),
    providing significant increase in throughput for enterprise
    class storage.

## Cons

-   If working in this mode the backup proxy will occupy the virtual
    infrastructure resources impacting consolidation ratio. This could
    ultimately require additional physical ESXi hosts and licensing.

-   This mode requires additional planning and configuration in the
    enterprise environments because of the additional large disk Hot-Add
    processes in VMware vSphere.

- 	In situations with a high number of VMware clusters with individual
	datastores a minimum of one proxy per cluster is needed, this can
    increase management overhead.

## Considerations and Limitations

Additional load is put on the vCenter Server and ESXi hosts as each disk
is mapped and unmapped (disk hot-add) at the backup proxies.

**Note**: For more information see vCenter Server connection overview
in the "Veeam Backup & Replication Server" section of this guide.

It may occur that VMware API reports that unmap and snapshot commit were
done correctly but a snapshot file still remains on disk. These
"orphaned snapshots" will grow over time and can fill up the datastore
leading to downtime. To mitigate the issue, Veeam implemented the following functionality:

-   Veeam Snapshot Hunter. This feature automatically initiates disk consolidation
    for VMs in the "Virtual machine disks consolidation is needed" state.
    For more information please see [Snapshot Hunter](./interaction_with_vsphere.md#snapshot-hunter)
    section

-   Bypassing Virtual Disk Development Kit (VDDK) processing to overcome some limitations and
    performance challenges, in particular:
    -   Veeam can back up multiple disks of VM in parallel on same proxy
    (default number is 4).
    - Typical "hot-add I/O bursts" during hot-add operations are mitigated by
    bypassing VMware VDDK during restores and replication.
    - When performing writes via hot-add and VDDK, excessive metadata updates on the VMFS datastore will occur. This significantly impacts performance for other workloads on the datastore, and slows down restore throughput. Bypassing VDDK helps overcoming this limitation

-   To avoid some VMware issues related to NFS datastore and hot-add
    processing (described at
    <https://kb.vmware.com/s/article/2010953>),
     enable a specific setting that will process VM backups only on
    backup proxies that run on the same host. For details see
    <https://www.veeam.com/kb1681>.
    To avoid this completely, it is recommended to use the Direct
    NFS backup mode for backup and restore of NFS datastore based VMs.

**Note:** For additional tips refer to the [Impact of Snapshot
Operations](./interaction_with_vsphere.md#Impact-of-Snapshot-Operations) section of this guide.

## vSphere 6.5 and Encryption

Virtual appliance mode is typically the best choice to ensure data
availability for vSphere 6.5 clusters with encrypted virtual machines.
In order to support backup of encrypted virtual
machines, the virtual backup proxy must be encrypted within the same encryption
domain (using the same KMIP server).

Backup modes Direct Storage Access and Backup from Storage Snapshots
are unavailable for encrypted virtual machines. NBD will be slower as virtual appliance mode as vSphere 6.5 also enforces SSL/TLS encryption for
network mode (NBD). Thus, virtual appliance mode will be the best performing choice, and it reduces host CPU load.

## Recommendations

-   Virtual appliance mode should be used when it is not possible to leverage
    Direct Storage Access, for example in the case of local datastores, Virtual
    Volumes (VVOL) or vSAN.

-   You will need at least one type of (virtual) SCSI controller added to
	  Proxy Server VM that is used somewhere at the VMs in your infrastructure
    to allow VMware to HotAdd the VM disks at backup.

-   Add an extra SCSI controller to allow for more VM disks processing
    in parallel (check the corresponding Veeam proxy settings, default
    value is 4). The limit for a single controller is the maximum number
    of devices per SCSI controller (15). Max SCSI controllers per
    VM is 4 = 60 disks max. Adding one additional SCSI controller is
    usually sufficient.

-   When deploying hot-add backup proxies avoid cloning existing
    VMs as this may lead to identical UUIDs and cause hot-add operations
    to fail.

-   You may re-use any existing Windows server VM (to save
    on licensing). The Veeam data mover process runs with ‘below normal’
    priority by default.

    **Note:** Changed block tracking (CBT) will be disabled for these
	hot-add proxies. Consider that it may impact the backup window in case
	the said virtual machines should be included in backup or replication
	jobs.

### Useful links
  * Specific client OS limitations for Hot-Add processing are documented in
  [Veeam Backup & Replication Release Notes](https://www.veeam.com/veeam_backup_9_5_u4_release_notes_rn.pdf),
  *
[Appliance Mode (Hotadd) Requirements and Troubleshooting](https://www.veeam.com/kb1054)
  * [How to test hotadd manually](https://www.veeam.com/kb1184)
