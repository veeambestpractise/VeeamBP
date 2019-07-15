# Proxy Servers - Intro

With backup proxies you can easily scale Veeam backup infrastructure
based on the organization demands:

-   In a **simple deployment** scenario for smaller
    environments or POC, the backup proxy is
    automatically installed on the Veeam backup server as part of the
    Veeam Backup & Replication installation.

-   In **advanced deployments**, the backup proxy role is manually
    assigned to one or more Windows servers. This approach allows
    for offloading the Veeam backup server, achieving better performance
    and reducing the backup window.

Backup proxies can be deployed both
in the primary site, where the backup server is located, or in a remote site
where additional infrastructure needs being backed up. A proxy server can be
installed on any managed Microsoft Windows server added to the backup
infrastructure. Depending on whether the proxy server is installed on a
physical or virtual machine, different transport modes are available.

A backup proxy handles data traffic between the vSphere or Hyper-V
infrastructure and Backup & Replication during backup,
replication (at source and target), VM copy, VM migration jobs or VM restore.
They are also used to detect and scan snapshots to enable Veeam
Explorer for Storage Snapshots features when any supported primary storage
is added to the backup server.

Backup proxy operations include the following:

-   Retrieving VM data from production storage

-   In-line source side data deduplication to skip whitespace and redundant
    blocks reported by vSphere Change Block Tracking (CBT), Veeam File
    Change Tracking (FCT) for Hyper-V versions from 2008 R2 to 2012 R2 or Resilient Change Tracking (RCT) for Hyper-V 2016.

-   Performing in-line compression and deduplication before sending
    it to the backup repository (for backup) or another backup
    proxy (for replication)

-   BitLooker: Applies to VMs running Windows OS and using NTFS. For more information, see the corresponding section of this guide > [Deduplication and Compression - BitLooker](../job_configuration/deduplication_and_compression.md#bitlooker)

- 	AES256 encryption, if enabled.

Technically a backup proxy runs a light-weight transport service that
takes a few seconds to deploy. When you add a Windows-based server to
Veeam backup management console assigning the proxy role to it,
Backup & Replication installs the necessary components, and starts the
required services on that server. Any host in a Hyper-V cluster is automatically
enabled as proxy server, when it is added to the infrastructure.
When a job is started, the backup server manages the dispatching of
tasks to proxy servers using its built-in [Intelligent Load Balancer](#intelligent-load-balancing) (ILB).

### Intelligent Load Balancing

To specify the threshold for proxy load an administrator uses the **Max
concurrent tasks** proxy setting (one task will be consumed for processing a single VM disk), Backup & Replication uses a unique load balancing
algorithm to automatically spread the load across multiple proxies. This
feature allows you to increase backup performance, minimize backup time
window and optimize data flow.

The default proxy server is configured for 2 simultaneous tasks at installation,
whereas subsequently added proxy servers analyze the CPU configuration. The proxy
server automatically proposes configuring 1 task per CPU core. During deployment,
it is determined which datastores or CSV the proxy can access. This information is stored
in the configuration database, and is used at backup time to automatically select
the best transport mode depending on the type of connection between the backup proxy and datastore.

After the algorithm identifies all existing backup proxies it distributes tasks
via the built-in Real-time Scheduler (RTS):

1.  It discovers the number of tasks being processed at the moment by
    each proxy and looks for the server with the lowest load and the
    best connection.

2.  All tasks are added to a "VMs to process" queue. When a
    proxy task slot becomes available, RTS will
    automatically assign the next VM disk backup task to it.

3.  Priority goes to the disk that belongs to an already
    processed VM, after that VMs of already running jobs have next higher
    priority.

**Tip:** At the repository, which writes the backup data, only one
thread is writing to the backup storage _per running job_. If few jobs
with a high number of VMs are processed simultaneously, you may experience
that these threads cannot fully utilize the available backup storage
performance. If throughput per I/O stream is a bottleneck, consider
enabling [per VM backup files](./repository_planning_pervm.md).

**Tip:** Default recommended value is **1** task per core/vCPU, with at least
2 CPUs. To optimize the backup window, you can cautiously oversubscribe the
**Max concurrent tasks** count, but monitor CPU and RAM usage carefully.

### Parallel Processing
Veeam Backup & Replication supports parallel processing of VMs/VM disks:

-   It can process multiple VMs within a job simultaneously, increasing
    data processing rates.

-   If a VM was created with multiple disks, Veeam will process
    these disks simultaneously to reduce backup time and minimize
    VMware snapshot lifetime.

- 	RTS gives priority to currently running parallel processes for VM disk backups.

To achieve the best backup window it is recommended to slightly oversubscribe the tasks slots, and start more jobs simultaneously. This allow Veeam to leverage the maximum of the task slots and lead into an optimal backup window.

**Note:** Parallel processing is a global setting that is turned on by default.
If you had upgraded from older versions please check and enable this setting.

### Backup Proxy Services and Components

Veeam backup proxy uses the following services and components:

-   **Veeam Installer Service** - A service that is installed and
    started on the Windows server once it is added to the list of
    managed servers in the Veeam Backup & Replication console. This
    service analyses the system, installs and upgrades necessary
    components and services.

-   **Veeam Transport Service** – A service responsible for deploying
    and coordinating executable modules that act as "data movers". It
    performs main job activities on behalf of Veeam Backup & Replication
    (communicating with VMware Tools, copying VM files, performing data
    deduplication and compression, and so on).

-   **VeeamAgent.exe process** - a data mover which can be started
    multiple times (on demand) for each data stream on the proxy.
    These processes can operate in either read or write mode. When used on a
    proxy server for backup, they are only performing read operations, while
    "write" mode is used for writing data on a target backup proxy
    (replication). Veeam agents in write mode are also used on all repository
    types, but will not be discussed in this chapter.
