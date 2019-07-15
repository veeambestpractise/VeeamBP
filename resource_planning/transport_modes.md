<!--- This was last Changed 03-05-17 by PS --->
# Transport Modes

Job efficiency and time required for its completion are highly dependent
on the data transport mode. Transport mode is a method used by the Veeam
proxy to retrieve VM data from the source host and write VM data to the
target destination.

## Direct Storage Access
In this mode, the backup proxy server has direct access to the storage volumes on
which VMs reside. When configured, the backup proxy will retrieve data directly from
the storage, bypassing the ESXi infrastructure.

Depending on storage protocols utilized, the proxy can be deployed as follows:

-   On a physical server for FibreChannel, FCoE, iSCSI or NFS
-   On a virtual machine for iSCSI and NFS

Both options can be used for [Backup from Storage Snapshots](./backup_from_storage_snapshots.md). When used with NFS
datastores or Backup from Storage Snapshots, Direct Storage Access mode will
also utilize the [Advanced Data Fetcher](./proxy_server_and_transport_modes.md#storage-optimizations).

## Virtual appliance mode

As the disks are hot-added, you may find the virtual appliance mode referred
to as `hotadd` in documentation and logs.

To work in this mode the backup proxy
must be deployed as a VM. For smaller deployments (e.g., several
branch offices with a single ESXi host per each office) you can
deploy a virtual backup proxy on a ESXi host that has access to all
required datastores. When backup or replication takes place and a VM
snapshot is processed the snapshotted disks are mapped to the proxy
to read data (at backup) and write data (at restore/replication);
later they are unmapped.

## Network mode

You may find network mode referred to as `nbd` in documentation and logs.

The most widespread backup method is network mode, which transports VM data through
the VMkernel interfaces of the VMware ESXi host on which the VM resides.

The benefit of using NBD is the fact that it requires no additional configuration,
and is supported regardless of physical or virtual proxy deployments, or storage
protocols used (including local storage, VMware Virtual Volumes or VMware vSAN). This is also the
reason NBD is used as the fallback method, in case Backup from Storage Snapshots,
Direct Storage Access or Virtual Appliance backup modes fail.

The only requirement is the proxy being able to access ESXi hosts on port
902/tcp. NBD backup throughput is typically limited to using up to 40% of the
bandwidth available on the corresponding VMkernel interfaces. If NBD-SSL is
enabled, the throughput is typically 10% slower than regular NBD. NBD-SSL is
_enforced_ for ESXi 6.5 hosts. Read more about this in
[Virtual Appliance Mode section - vSphere 6.5 and encryption](./virtual_appliance_mode.md#vsphere-65-and-encryption).

Starting from vSphere 6.5b (EXSi build 5146846 and VDDK libraries version shipped with Veeam B&R update 3) unencrypted is available again and encrypted VMs can be backed up using regular NBD mode.
[More info regarding the content of the VMware vSphere update can be found here.](https://pubs.vmware.com/Release_Notes/en/developer/vddk/65/vsphere-vddk-650b-release-notes.html)

_The following sections explain transport modes in detail._
