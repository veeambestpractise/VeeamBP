<!--- This was last Changed 03-05-17 by PS --->
## Sizing For Wan Acceleration
When configuring the WAN accelerator on the source side, consider that all VM disk data blocks are already in the source backup repository and they can simply be re-read from the source repository when needed. This is the reason why configuring the cache size on a source WAN accelerator is not as important but still must exist as a number. It is never used for caching any data. However, there are other files residing in the source WAN accelerator folder, and the file structure will be described in the following sections.

##### Hardware
The source WAN accelerator will consume a high amount of CPU and memory whilst re-applying the WAN optimized compression algorithm. Recommended system configuration is 4 CPU cores and 8 GB RAM. When using an existing Veeam Managed Server for Wan Acceleration which already has a role such as Veeam Backup & Replication Server, Proxy or windows Repository ensure you have not overcommitted the CPUs on that host and there is resource for each source and Target Wan Accelerator. If there is not enough CPU cores free the job will wait for a free cpu to continue.

![Source WAN accelerator IOPS](./wan_acceleration_source_io.png)

The I/O requirements for the source WAN accelerator spikes every time a new VM disk starts processing. Thus, it is recommended to deploy WAN accelerators
on disk configurations with decent I/O performance.

![Source WAN accelerator IO size](./wan_acceleration_source_io_pattern.png)

The typical I/O pattern is made of many small blocks, so using high latency spinning disks is not recommended.

##### Disk Size
Each digest file consumes up to 2% of its source VM disk size. This means, for example, that a 2 TB VM disk file can produce a digests file up to 40 GB in size.

Additionally, plan for 10 GB of working space for payloads and other temporary files.

- Formula: `(<Source data size in GB> * 2%) + 10 GB`

- Example with 2 TB source data: `(2,000 GB * 2 %) + 10 GB = 50 GB`

For understanding how disk space is consumed, please see the following sections.

**Note:** As the cache size on the source WAN accelerator will always be ignored, the digests file will be produced regardless of cache setting been configured. They may consume considerable disk space.

##### VeeamWAN\GlobalCache\src
Only a `data.veeamdrf` file is located in the `\VeeamWAN\GlobalCache\src` folder. This file will be synchronized _from_ the target WAN accelerator during the very first job run (or if the cache was manually cleared) to understand what data blocks are already
cached in the target WAN accelerator. The size of this file is typically up to 2% of the configured target cache size; thus, it may take some
time for the initial data transfer to begin.

##### VeeamWAN\Digests
On the source WAN accelerator there are the VM disk digests that take up disk space. For each processed VM disk, a disk digest file is created and placed in `\VeeamWAN\Digests\<JobId>_<VMId>_<DiskId>_<RestorePointID>`.

**Note:** Although the Digest folder is created on the target accelerator no data is stored on the target normally, however it must be sized into the target in case the digest on the source becomes corrupt or is missing. In this case the target will calculate its own digests in this location until the source WAN Accelerator comes back online.

 Traffic throttling rules should be created in both directions. See [Network Traffic Throttling and Multithreaded Data Transfer](https://helpcenter.veeam.com/docs/backup/vsphere/setting_network_traffic_throttling.html?ver=95) for more information.

### Target WAN Accelerator

The following recommendations apply to configuring a target WAN accelerator:

-   The cache size setting configured on the target WAN accelerator will be applied to the pair of WAN accelerators. This should be taken into account when sizing for many-to-one scenarios, as configuring 100 GB cache size will result in 100 GB multiplied by the number of pairs[^1] configured for each target WAN accelerator.

-   It is recommended to configure the cache size at 10 GB for each operating system[^2] processed by the WAN accelerator. 

-   Once the target WAN accelerator is deployed, it is recommended to use the cache population feature (see [this section](https://helpcenter.veeam.com/docs/backup/vsphere/wan_population.html?ver=95) of the User Guide for details). When using this feature, the WAN accelerator service will scan through selected repositories for protected operating system types.

-   It is also possible to seed the initial copy of data to the target repository to further reduce the amount of data that needs to be transferred during the first run.

![Populate Cache](../media/image24.png)

#### Sizing

##### Hardware
Although a target WAN accelerator will consume less CPU resources than the source, the I/O requirements for the target side are higher.

For each processed data block, the WAN accelerator will update the cache file (if required), or it may retrieve the data block from the target repository
(if possible). As described in the user guide, the cache is active on operating system data blocks, while other data blocks are being processed only with the WAN optimized data reduction algorithm (in-line compression).



![Target WAN accelerator IOPS](./wan_acceleration_target_io.png)

Tests show that there are no significant performance differences in using spinning disk drives as storage for the target WAN accelerator cache rather than flash storage. However, when multiple source WAN accelerators are connected to a single target WAN accelerator (many-to-one deployment), it is recommended to use SSD or equivalent storage for the target cache, as the I/O is now the sum of all the difference sources.

##### Disk Size
Ensure that sufficient space has been allocated for global cache on the target WAN accelerator.

At least 10 GB per each different OS that is backed up. That is, if you plan to backup VMs running Windows 8, Windows 2008 R2, Windows 2012 and RHEL 6 (four different operating systems), you will need at least `10 GB * 4 = 40 GB`

Plan for additional **20 GB** of working space for cache population, payload and other temporary files.

If the cache is pre-populated, an additional temporary cache is created. The temporary cache will be converted into being the cache used for the first connected source. Subsequently connected sources will duplicate the cache of the first pair. As caches are duplicated the configured cache size is considered **per pair** of WAN accelerators.

**Formulas:**

- Formula for configured cache size (insert this number in configuration
  wizard):
  - `(Number of operating systems * 10 GB) + 20 GB`
- Formula for used disk space:
  - `(Number of sources * <formula for configured cache size>)`

**Examples:**
- Example with one source and two operating systems:
  - Configured cache size: `(2 operating systems * 10 GB) + 20 GB = 40 GB`
  - Used disk space: `(1 source * 40 GB) = 40 GB`
- Example with five sources and four operating systems:
  - Configured cache size: `(4 operating systems * 10 GB) + 20 GB = 60 GB`
  - Used disk space: `(5 sources * 60 GB) = 300 GB`

Digest space must be built into the equation using the same size for each source target:

- Example with one source two operating systems
  - one source digest space 20GB equates to target digest requiring 20GB
  - so 20GB + Cache disk space '(2 operating systems * 10 GB) 20GB' is 40GB


- Example with 5 source  
  - Five source with digest space 20GB each equates to target digest requiring 20GB * 5, 100GB
  - so 100GB + Cache disk space '(2 operating systems * 10 GB * five sources) 100GB' is 200GB

For understanding how the disk space is consumed, please see the following sections.

##### VeeamWAN\GlobalCache\trg

For each pair there will be a subfolder in the `trg` directory, with a UUID describing which source WAN accelerator the cache is attached to. In each of those subfolders, the `blob.bin` file containing the cache will be located. That file size corresponds to the setting configured in the management console.

**Note:** The `blob.bin` file will exist for all connected source WAN accelerators.

##### VeeamWAN\GlobalCache\temp
When connecting a new source WAN accelerator, the `temp` folder will temporarily contain the `data.veeamdrf` file that is later transferred to the source containing the cache manifest.
