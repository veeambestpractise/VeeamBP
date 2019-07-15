## Configuration Guidelines

### Parallel Processing
A repository can be configured to limit the amount of parallel tasks it can process at a time; with parallel processing enabled (by default) a *task* is one VMDK handled by the proxy during a backup job, or by a repository during a backup copy job. If there are many parallel tasks on the proxy side for only few tasks on the backup repository, this will lead the Veeam scheduler service to wait for available resources on the repository. To prevent such situation, you can figure out on which side the bottleneck will be (proxy or repository) and then set the overall amount of parallel tasks on the proxies equal to the total amount of parallel tasks on the repositories.

**Note:** Consider tasks for read operations on backup repositories (like backup copy jobs).

### General guidelines for virtual repositories
To right sizing a backup repository, consider the following:

- Each vCPU core should have no more than 2 concurrent tasks loaded into it
- For each vCPU, you need to count 4 GB of memory
- With bigger machines, also network limits come into play , and that’s another reason to build many smaller repositories

Suppose you have a VM with 8 vCPU. You need 32Gb of memory, and this repository could be able to handle up to 16 concurrent tasks (we can go higher, but that’s a good starting point). Now, in general we say that one task doing incremental backups runs at about 25 MB/s, that is 200 Mbit/s. If the VM has the usual vmxnet3 link, that’s 10Gb and divided by 200 Mbit/s it gives you a bottleneck at around 50 tasks, that would be 25 vCPU. So, it is not recommended to go above this size or you may end up to overload the network.

Also take into account that multiple virtual repos may be running over the same physical ESXi and its links, so you also need to consider using anti-affinity rules to keep those repos away from each other.

### SOBR
For any type of extent, and also for ReFS, we tend to suggest 200TB as the biggest size. Even though some customer go even bigger where a physical server is involved, we recommend to not go too big to avoid potential failures (read also downtime, not just damages). Smaller server equal to smaller failure domains.
This goes into combination with what written above, so if you need for example 600TB of usable space, then you know you need  3 extents. Sometime this number is bigger, since for example people using SAN as the source for their volumes can only create up to 64TB volumes, so this becomes the biggest size of a single extent. This is also true for virtual repositories when a VMDK is used,unless you want to use RDM (which we are fine with).

When using SOBR along with ReFS extents make sure you select data locality policy to enable block cloning.
With performance policy the backup chain gets split, incrementals and fulls are placed on different extents. ReFS requires all the restore points to be on the same extent.

### Blocks sizes

During the backup process data blocks are processed in chunks and stored inside backup files in the backup repository. You can customize the block size during the [Job Configuration](../job_configuration/deduplication_and_compression.html#deduplication) using the **Storage Optimization** setting of the backup job.

By default block size is set to **Local target**, which is 1 MB before compression. Since compression ratio is very often around 2x, with this block size Veeam will write around 512 KB or less to the repository per block.

This value can be used to better configure storage arrays; especially low-end storage systems can greatly benefit from an optimized stripe size.

There are three layers where the block size can be configured: Veeam block size for the backup files, the Filesystem, and the Storage volumes.

Let's use a quick example:

![Layers of block sizes](block-sizes-layers.png)

The Veeam block size of 512KB is going to be written in the underlying filesytem, which has a block size of 64k. It means that one block will consume 8 blocks at the filesytem level, but no block will be wasted, as the two are aligned. If possible, set the block size at the filesytem layer as close as possible to the expected Veeam block size.

Then, below the filesytem there is the storage array. Even on some low-end storage systems, the block size (also called stripe size) can be configured. If possible, again, set the stripe size as close as possible to the expected Veeam block size. It's important that each layer is aligned with the others, either by using the same value (if possible) or a value that is a division of the bigger one. This limits to a minimum the so called **write overhead**: with a 128KB block size at the storage layer, a Veeam block requires 4 I/O operations to be written. This is a 2x improvement compared for example with a 64KB stripe size.

**Tip:** As can be seen from the field, optimal value for the stripe size is often between 128 KB and 256 KB; however. It is highly recommended to test this prior to deployment whenever possible.

For more information, refer to this blog post: <https://www.virtualtothecore.com/veeam-backups-slow-check-stripe-size/>

### File System Formats
In addition to the storage stripe size alignment, as explained in the previous paragraph, the file system may also benefit from using a larger cluster size (or Allocation Unit Size). For example, during formatting of NTFS volumes, Allocation Unit Size is set to 4KB by default. To mitigate fragmentation issues, configure to 64 KB whenever possible.

It is also recommended to use a journaling file systems (this makes exFAT a less reliable option than NTFS).

### Using "Large File" Switch for NTFS
A file size limitation can be occasionally reached on NTFS, especially on Windows Server with deduplication enabled. This happens due to a hard limit reached on the file records size because of the  high level of file fragmentation. To mitigate the issue, we recommend to format Windows NTFS repositories with the "**/L**" (large files) option.

### Keeping File Size Under Control
Try to avoid backup chains growing too much. Remember that very big objects can become hardly manageable. Since Veeam allows a backup chain to be moved from one repository to another with nothing more than a copy/paste operation of the files themselves, it is recommended to keep backup chain size (the sum of a single full and linked Incrementals) under 10 TB per job (\~16TB of source data). This will allow for a smooth, simple and effortless repository storage migration.

### Synthetic Backup and Caching

To get the best out of a synthetic backup and enhance the performance, it is recommended to use a write-back cache. Read and write request processing with write-back cache utilization is shown in the figure below.

![](../media/image13.png)
