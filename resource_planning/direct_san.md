# Direct Storage Access

Direct Storage Access covers two transport modes: VDDK based "Direct SAN", and
"Direct NFS" which utilizes a proprietary Veeam NFS client. Direct NFS also
utilizes [Advanced Data Fetcher](./proxy_server_and_transport_modes.md#storage-optimizations) (ADF).

The Direct SAN mode uses a direct data path (Fibre Channel or iSCSI) between
the VMFS datastore and the backup proxy for data transfer. The proxy requires
read access to the datastores so Fibre Channel zoning or iSCSI initiator configuration
and LUN masking on the storage array must reflect this.
In most cases, the Veeam backup proxies are added to
the same "host group" on the storage as the existing ESXi hosts, in order to
ensure all LUNs are masked correctly.

To use Direct NFS backup mode, the proxies need access to the NFS network
and must be configured in the NFS server's "exports" for read and/or write
access. As NFS based storage uses IP, the real-time scheduler (RTS) will ensure
to always use the nearest backup proxy (by means of the fewest network "hops"). This is especially useful if the NFS network traffic has to cross IP routing devices.

If write access is provided, Veeam will automatically perform full VM restore
via Direct Storage Access for thick provisioned VMs.

## Pros

-   Direct Storage Access mode provides very fast and the most reliable
    predictable backup performance (typically using 8 Gb Fibre Channel
    or 10 GbE for iSCSI and NFS).

-   Produces zero impact on vSphere hosts and VM production networks for backup data transport.

-   It is possible to perform full VM restore using Direct Storage Access. This mode will be used automatically if eligible backup proxies are available in the backup infrastructure and if the VM disks are thick provisioned.

-	Direct Storage Access is the fastest backup and restore mode for NFS datastores. It uses multiple concurrent read and write streams with an increased queue depth via ADF.

- Direct Storage Access for NFS datastores will mitigate the "VM stun" issues that may be caused by Virtual Appliance Mode (hot-add).

-   Direct Storage Access for FC and iSCSI can be used for replication at the target for the initial replication (with thick provisioned disks) only. For NFS datastores, Direct Storage Access can be used for initial and incremental replication passes. There are no differences on the source replication proxy.

## Cons

-   Typically, Direct Storage Access requires a physical server for Fibre
	Channel, iSCSI or NFS connection. For virtual only deployments, Direct Storage
  Access for iSCSI and NFS is possible, but would transport the data through
  networks of the ESXi hosts, typically making hot-add the more efficient choice.

-   Restore via Direct Storage Access using Fibre Channel or iSCSI is possible only
	  for thick-provisioned VM disks. At restore the data stream needs to be
    coordinated in the background with vCenter or an ESXi host which can slow down the restore speed. Consider adding additional hot-add proxy servers for restore (FC/iSCSI only).

-   Direct SAN mode (FC/iSCSI only) is the most difficult backup mode to
	configure as it involves reconfiguring not only the storage but also the SAN, (Fibre Channel zoning, LUN masking, or reconfiguration of iSCSI targets) to provide the physical proxy server(s) with direct access to the production VMFS datastores. When such configuration has been implemented it is extremely important to ensure that HBAs, NIC drivers and firmwares are up-to-date and that multi path driver software (e.g. MPIO) is properly configured.

For more information about configuring Direct Storage Access refer to FAQ
at [Veeam Community Forums: Direct Storage Access
Mode](https://forums.veeam.com/vmware-vsphere-f24/vmware-frequently-asked-questions-t9329.html)

## Example

If datastores or virtual raw device mapping (vRDM) LUNs are connected via shared storage
using Fibre Channel, FCoE or iSCSI, you may add a backup proxy as a member to
that shared storage using LUN masking. This will allow for accessing
the storage system for backup and restore.

Ensure that a connection between the storage and backup proxy can be established. Verify FC HBAs, zoning, multipath, driver software and iSCSI configurations including any network changes. To test the connection, you may review volumes visible in Windows Disk Management (as offline), adding one disk per storage system at a time. Once the initial connection has been verified, add the remaining volumes for that storage array.

## Recommendations

-   Use the multipath driver software of the storage vendors choice
    (preferred integration into Microsoft MPIO) to avoid disk or cluster
    failovers at storage level. This will also prevent the whole storage
    system from being affected by possible failovers if wrong data paths
    are used. It is highly recommended to contact the storage vendor for
	  optimal settings.

-   If you attach a large number of volumes to the backup proxy, consider
    that logging for the process of searching for the correct volume during the
    job run can require extra processing time per VM disk (as well as for
    overall volume count). To avoid Veeam logging becoming a bottleneck
    you can disable logging for this particular task this with the following
    registry setting:

  -   Path: `HKEY_LOCAL_MACHINE\SOFTWARE\Veeam\Veeam Backup and Replication`
  -   Key: `VDDKLogLevel`
  -   Type: REG_DWORD
  -   Value: 0 (to disable)
  -   Default: 1

  **Note**: As this reduces the amount of information in debug logs,
	remember to enable it again when working with Veeam support (to
	facilitate debugging of Direct Storage Access related challenges).

-   To achieve performance/cost optimum, consider using fewer proxies with
    more CPU cores available. This will help to fully utilize the HBA or
    NIC capacity of each proxy server. A 2 CPU System with 2x 12 cores is
    considered a good configuration balanced between throughput and costs.

## Security Considerations for Direct SAN

During deployment of the proxy role to a Windows VM, Backup &
Replication uses the following security mechanisms to protect them:

-   Windows SAN Policy is changed to "Offline (shared)". This prevents
    Windows from automatically bringing the attached volumes online and
    also prevents Windows write operations to the volumes. During Direct
    SAN restore, if the disks are offline, the proxy will attempt bringing the
    volume online, and verify that it is writeable. In case the operation
    fails, restore will failover to using NBD mode through the same proxy.

-   Veeam deploys VMware VDDK to the backup proxy. In most
    cases, VDDK coordinates read and write operations (Direct SAN restore) with VMware vSphere allowing VMware's Software to control
    the read and write streams in a reliable manner.

If necessary, you can take additional measures as follows:

- 	Disable automount. Open an elevated command prompt
    and disable automount using the following commands:

```
diskpart
automount disable
```

-   Disable Disk Management snap-in with:

    **Group Policy\User Configuration > Administrative Templates > Windows Components > Microsoft Management Console > Restricted/Permitted snap-ins > Disk Management**.

-   Restrict the amount of users with administrative access to proxy servers.

-   Present LUNs as read-only to the backup proxy server. This
    capability is supported by most modern storage. When possible, implement
    read-only LUN masking on the storage system or read-only zoning on the
    Fibre Channel switches (possible on most Brocade variants).

If a VMFS datastore is manually brought online in Windows Disk Management by
mistake, and disk resignaturing is initiated, the datastore will become unavailable,
and VMs will stop. Please contact VMware Support for assistance with recreating
the VMFS disk signature. For more information on Windows re-signaturing process
and VMware datastores please refer to [VMware KB1002168: Unable to access the VMware virtual machine file system datastore when the partition is missing or is not set to type fb](https://kb.vmware.com/s/article/1002168)

## Summary

Use Direct Storage Access whenever possible for fast backups and reduced load on the ESXi hosts. Consider using hot-add proxies, as these typically restore faster than Direct SAN restores. Direct SAN uses VDDK, which can cause excessive metadata updates while hot-add restores bypass VDDK.

For NFS datastores, Direct NFS is the best choice for both backup and restore. It delivers the highest possible throughput, without any negative side effects. You can use it for virtual and physical proxy deployments.
