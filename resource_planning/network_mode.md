# Network Mode

Network mode is by far the easiest backup mode to implement as it
requires no additional configuration. With this mode, Veeam uses the same interface to inspect, backup and restore VMware configuration files as well as to read Change Block Tracking (CBT) information.

In this mode, the backup proxy will query vCenter for the name of the ESXi host on which
the VM scheduled for backup resides. Typically, hosts are added to vCenter using
FQDN, which means NBD relies heavily on properly working DNS resolution. Regardless if the ESXi hosts are
connected to vCenter using a VMkernel interface on an isolated management network,
VADP backup solutions will attempt to connect to this same interface. Please see
the section on [DNS Resolution](./dns_resolution.md) for more information on how
to override the default interface used for NBD backups.

As the only prerequisite, the backup server and proxy server requires
ports 443/tcp and 902/tcp being open to the ESXi hosts.

**Note**: It is highly recommended to maintain a good network connection
between the VMware ESXi VMKernel port and Veeam Backup & Replication as
it will be used by many other features like Instant VM Recovery, Virtual
Lab and SureBackup, Linux FLR appliance, config files backups etc.

For load balancing, Veeam uses a selection of proxy servers based on the
network subnet:

-   Backup proxies in the same subnets as the VMKernel interfaces are selected
    if you have the **Automatic Selection** proxy setting configured in the
    backup jobs.

    ![](../media/image10.png)

-   If no proxy servers are available within same subnet as the VMKernel
    interface of the ESXi host, you may have to manually select the
    proxies that are most suitable to process the backup job. It is recommended not to use **Automatic selection** in such scenarios, as proxies might be selected which would transfer data across too many network hops (or even across WAN links). You can manually select all eligible proxies to enable load balancing.

    ![](../media/image11.png)

-   In case you work with several branches or datacenter environments
    it is also recommended that you manually choose the proxies
    (per site) in the job settings to reduce the time spent by the
    Real Time Scheduler to determine eligible backup proxies.

## Pros

-   Network mode can be used for both backup and restore with same speed.

-   Works with both physical and virtual backup proxies.

-   Being the most mature of all transport modes, it supports all types
    of storage.

-   Is recommended for NFS based storage in cases where Direct NFS is unavailable.
    Using NBD will minimize VM stunning. See also the
    "[Considerations for NFS Datastores](./interaction_with_vsphere.md#considerations-for-nfs-datastores)"
    section of this guide.

-   Performance on 10 GbE VMkernel interfaces typically provide around 400-500 MB/s
    of throughput per host.

-   As data transfers initiate very quickly, network mode is
    preferable for processing incremental backups on relatively static
    virtual machines (VMs generating a small amount of change).

-   It can be helpful when dealing with many clusters with individual
    storage configurations (e.g. hosting providers). In such
    deployments, using network mode for data transfer can help
    reducing Veeam footprint and costs as well as to increase
    security (if compared to other modes and storage configuration).

## Cons

-   Typically, network mode uses only up to 40% of the available
    bandwidth of the external VMKernel interface due to
    throttling mechanisms implemented on the management interfaces.

-   It can be even slower on 1 Gb Ethernet (about 10-20 MB/s) due to
    throttling mechanisms, so especially restores via network mode can
    take very long.

**Tip**: Please see the section on [DNS Resolution](./dns_resolution.md) for
information on how to override the network interface used for NBD backups e.g.
when both 1 GbE and 10 GbE VMkernel interfaces are available. It is preferred
to force usage of 10 GbE for highest possible throughput in such cases.

## Recommendations

When you choose network mode (NBD), you entirely avoid dealing with hot-add
vCenter and ESXi overhead or physical SAN configuration. NBD is a very fast
and reliable way to perform backups. In emergency
situations when you need fast restore the following tips can be helpful:

-   Consider setting up at least one virtual backup proxy
    for hot-add based restores. This will result in
    higher throughput and thus lower RTO.

-   Conside  restoring to a thin disk format and later use standard
    VMware methods to change the disk format to thick disk if needed,
    as thin disk restores have to transport less data.

-   Another way to speed up restores is using Instant VM
    Recovery with Storage vMotion (if license is available) as it is not
    affected by the same throughput limitations as the VMkernel interfaces.

When using NBD for backup, please consider the following:

-   As there is no overhead on backup proxies (like SCSI hot-add or
-   searching for the right volumes in Direct Storage Access),
-   network mode can
    be recommended for scenarios with high-frequency backups or
    replication jobs, as well as for environments with very low overall
    data and change rate (VDI).

-   To protect VMware, Veeam reduces the number of permitted NBD connections
    to 28. Please see the corresponding section in
    [Interaction with vSphere](./interaction_with_vsphere.md#vcenter-server-connection-count)
    for more information on how to alter the configuration using registry keys.
