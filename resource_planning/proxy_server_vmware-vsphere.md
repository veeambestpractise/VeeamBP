# Proxy Server - VMware vSphere

Like any backup vendor using VMware vStorage API for Data Protection (VADP),
Backup & Replication is using the VMware Virtual Disk Development Kit (VDDK) within the Veeam Transport Service. This is necessary for management interaction with
vCenter and ESXi hosts, while in some scenarios, VDDK is bypassed in favor of
Veeam [Advanced Data Fetcher](#advanced-data-fetcher) for performance reasons.

### Storage optimizations
Stock VDDK transport modes have some limitations, such as being unable to process
multiple disks in parallel when using [virtual appliance transport mode](./virtual_appliance_mode.md) (hot-add), introducing excessive VMFS metadata updates when performing replication, or being unable to backup from NFS based datastores.
To overcome these limitations, Veeam introduced logic to bypass VDDK, when it is
more optimal to do so.

### Veeam Advanced Data Fetcher (ADF)
Veeam Advanced Data Fetcher (ADF) adds increased queue depth for >2x read
performance on enterprise storage arrays. ADF is supported for Backup from
Storage Snapshots, Direct NFS and virtual appliance mode.

Other enhancements include:
- a proprietary NFS client for backing up VMs on NFS datastores
- parallel processing of multiple VM disks when backing up via hot-add
- parallel processing of multiple VM disks during restore
- bypass VDDK when performing replication or VM restores via hot-add, to avoid excessive VMFS metadata updates
- allow restore via Direct SAN

### Intelligent Load Balancing
When it comes to distribute the workload in VMware vSphere environments, first Backup & Replication checks if data processing can be
assigned to a backup proxy with the following priority:

1. Direct Storage Access (which includes VDDK based Direct SAN or Veeam proprietary Direct NFS).
2. Virtual appliance mode (hot-add)
3. Network Block Device (NBD)

For more details, see the [Transport Modes](./transport_modes.md) section of this guide.
