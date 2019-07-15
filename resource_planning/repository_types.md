<!--- This was last Changed 03-05-17 by PS --->
# Repository Type
Being storage-agnostic, Veeam Backup & Replication supports a wide range of repository types, each offering its own set of specific capabilities. So when deciding on repository storage, you might consider the following:
-   Capacity
-   Write performance
-   Read performance
-   Data density
-   Security
-   Backup file utilization

As a basic guideline, a repository should be highly resilient, since it is hosting customer data. It also needs to be scalable, allowing the backup to grow as needed.

Organization policies may require different storage types for backups with different
retention. In such scenarios, you may configure two backup repositories:
-   A high-performance repository hosting several recent retention points for instant restores and other quick operations
-   A repository with more capacity, but using a cheaper and slower storage, storing long-term retention points

You can consume both layers by setting up a backup copy job from the first to the second repository, or leverage Scale-out Backup Repository, if licensed.

## Server-Based Repository: DAS or SAN?

### Direct-Attached Storage (DAS)
This is an easy, fast and lowcost way to use storage. It is a new approach to use microsegmentation instead of monolithic solutions. The DAS approach is in terms of performance a very fast solution. It can be used as a dedicated system to one Cluster or in a Scale-out Backup Repository. DAS is a normal industry standard x64 server with a bunch of disks attached to it. 
-   It is recommended to use a performant RAID controller with local battery cache. Be aware of any RAID overhead when designing a DAS soltuion. Typically RAID 6/60 (depends on the amount of disks) is recommended (IO overhead of factor 6). The Stripe Size should be 256KB or greater.
-   Since a DAS storage can be fully dedicated to backup operations, this type of repository is considered to offer a good balance between “performance” and “cost” factors.
-   A strong benefit of a DAS repository is that it supports the features offered by Veeam Backup & Replication in a very flexible way. In particular, it provides good read and write performance, sufficient for Veeam vPower-based features (such as Instant VM Recovery, SureBackup, and others). As it typically provides good random I/O performance, it will be the optimal solution when using I/O intensive backup modes such as reverse incremental or forever forward incremental (also used in backup copy job).
-   For scalability you can scale vertical (more disks in an enclosure or additional) and horizontal (more servers, if e.g. the network throuput is reached, the SAS channels are saturated, more IOPS are needed for restore reasons) 


**Tip:** When using Microsoft based repositories, use the RAID controller, to build the RAID set and set the Stripe Size there. Don't us any kind of Software or HBA based RAID Level.

| Pros               | Cons                                          |
|:-------------------|:----------------------------------------------|
| Cost               | single Point of Failure is the RAID Controller|
| Performance        |                                               |
| Simplicity         |                                               |
| Microsegmentaion   |

### SAN Storage

This is an advanced and manageable solution that offers the same advantages as DAS, and adds more advantages like higher availability and resiliency.

The volume size and quantity are easily adjustable over time, thus offering a scalable capacity.

**Tip**: You can configure multiple backup repositories on the SAN storage to increase repository throughput to the storage system.

| Pros                   | Cons       |
|:-----------------------|:-----------|
| Reliability            | Complexity |
| Performance            | Cost       |
| Technical capabilities | Monolithic approach     |

## Windows or Linux?
The main difference between Windows and Linux in regards to Veeam repositories is the way they handle NAS shares – this can be summarized as a choice between NFS and SMB. It depends on your IT infrastructure and security what is better to manage and to maintain.

## Physical or Virtual?
You can use a virtual machine as a repository server, however, keep in mind that the storage and associated transport media will be heavily occupied.

If you are using a SAN storage, it can be accessed through software iSCSI initiators, or directly (as a VMDK or RDM mounted to the Repository VM).

Best practice is to avoid using the same storage technology that is used for the virtualized infrastructure, as the loss of this single system would lead to the loss of both copies of the data, the production ones and their backups.

In general we recommend whenever possible to use physical machines as repositories, in order to maximize performance and have a clear separation between the production environment that needs to be protected and the backup storage.

## NTFS or ReFS?
You can use both filesystems from Microsoft as filesystem for a Veeam Repository. Both filesystems have different behaviour during different backup situations.
 
### NTFS:
When using NTFS please make sure that
- the volume is formatted with 64KB block size

Be aware of the following points during synthetic operations
- NTFS will read and write all blocks during a merge or synthetic full operation, which will result in a very high IO load and a high resulting queue length of the storage system
- The highest impact to disk queue length will be in a per VM mode merging an incremental in FFI or Reverse Mode

### ReFS:
ReFS is using linked clone technology. This is perfect for synthetic operations and will save dramatic IOs and throughput during operations like merges or creating synthetic fulls.

When using ReFS please make sure that
- the volume is formatted with 64KB block size
- check https://docs.microsoft.com/en-us/windows-server/storage/refs/refs-overview
- Configure 256 KB block size on LUNs (Storage or RAID Controller)
- never bring linked clone space savings into your calculation for required storage space
- make sure your server has 1 GB RAM per 1 TB used on repository, add additional 8 GB for the Windows Server operating system.
- „All ReFS supported configurations must use Windows Server Catalog certified hardware” - please contact your hardware vendor
- Never use any shared LUN concept with ReFS and a Veeam Repository 
- Check the existing driver version of ReFS. The minimum should start from ReFS.sys 10.0.14393.2097
- ReFS will flush metadata during synthetic processes to the disk very pushy. These meta data flushes are based on 4KB blocks. Your controller and disk system should be able to handle these OS related system behaviours.


## SMB Share

When using a SMB share as target please check the following points

- SMB 3.x.x must be fully supported by the storage vendor or Windows Server (recommended Windows Server 2016+)
- To improve performance and reduce the latency impact, use one of the RDMA features Windows Server provides with SMB direct. RoCE or iWarp.
- a 10 Gibt/s network interface can be saturated with modern CPUs. If the repository is able to write faster than consider 40 Gbit/s connections between source and repository
- Try to avoid to many routing hops between source and Veeam Repository this will add latency and reduce your performance
- When an application writes data to an SMB share using WinAPI, it receives success for this I/O operation prematurely - right after the corresponding data gets put into the Microsoft SMB client's sending queue. If subsequently the connection to a share gets lost – then the queue will remain in the memory, and SMB client will wait for the share to become available to try and finish writing that cached data. However, if a connection to the share does not restore in a timely manner, the content of the queue will be lost forever.