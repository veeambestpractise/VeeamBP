<!--- This was last Changed 03-05-17 by PS --->
# WAN Acceleration

By combining multiple technologies such as network compression, multi-threading, dynamic TCP window size,
variable block size deduplication and global caching, WAN acceleration provides sufficient capability when the network bandwidth is low or dramatically reduced when performing Backup Copy and Replication jobs. This technology is specifically designed to accelerate Veeam job. Any other WAN acceleration technology should be disabled for Veeam traffic.

To determine whether WAN acceleration is necessary in an environment, it is important to understand what particular savings can be achieved.

## Determining Required Bandwidth

When using WAN acceleration on links with low bandwidth, you may have to manually seed the initial copy to the target. For more information, refer to the [WAN Acceleration](https://helpcenter.veeam.com/docs/backup/vsphere/wan_acceleration.html?ver=95) section of the Veeam Backup & Replication User Guide.

The WAN accelerator uses its own digests based on the hashes of the blocks inside a VM disk, which means that it reads data from the backup files and re-hydrating them on the fly, or it reads directly from the source VM in case of replication. The WAN accelerator
component will then process those data blocks with much more efficient data deduplication and compression algorithms. This is the reason why the WAN
accelerator consumes significant amounts of CPU and RAM resources.

To determine how much data has to be transferred over the WAN link with and without WAN acceleration enabled in a backup copy job, you can compare
the daily changes of the primary backup job statistics (as the same data is transported in a standard backup copy job without WAN acceleration)
with the WAN accelerated backup copy job log and statistics.
