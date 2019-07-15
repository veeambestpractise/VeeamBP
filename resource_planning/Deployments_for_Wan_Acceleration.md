
<!--- This was last Changed 03-05-17 by PS --->
## How Many WAN Accelerators to Deploy?
As the source WAN accelerator can only process one task at a time (one VM disk in a backup copy job or replication job), you may need to deploy multiple WAN accelerator pairs to meet the performance demands.

As the target WAN accelerator can handle multiple incoming streams (as described in the [Many-to-One WAN Acceleration](https://helpcenter.veeam.com/docs/backup/vsphere/wan_acceleration_many.html?ver=95) section of the User Guide), it is recommended to maintain a 4:1 ratio
between the number of source WAN accelerators per target WAN accelerator.

This guideline is very much dependent on the WAN link speed. Many source sites with low bandwidth will create little pressure on the target WAN accelerator. So, for instance, in multiple ROBO configurations a 10:1 ratio can be considered.

If there are sites with very high bandwidth (such as
datacenter-to-datacenter replication), they will produce a much more significant load on both the target WAN accelerator and the target repository due to the second data block lookup (for more information, refer to the [User Guide](https://helpcenter.veeam.com/docs/backup/vsphere/wan_acceleration_sources.html?ver=95)).

**Note:** The secondary data block lookup is used, when a data block is not available in the WAN accelerator cache. When there is a WAN cache “miss”, the secondary lookup for the same data block is performed on the target repository. If it is found here, it is read back to the WAN accelerator instead of re-transmitting over WAN.

Assuming the source and target repositories can
deliver the throughput required for the optimal processing rate, use the guidelines that follow.

**Note:** The numbers below are processing rates. The WAN link usage is dependent on the achieved data reduction ratio.

-   Average throughput per target WAN accelerator: 500 Mbit/s (62.5 MB/s)

-   Depending on the achieved data reduction rate (typically 10x), the transfer rate over the WAN link will vary.

    -   If the processing rate is 62.5 MB/s, and the data reduction rate is 10x, then it is possible to sustain 6.25 MB/s (50 Mbit/s) over the WAN link.

    -   If the WAN link has high bandwidth (above 100Mbps) consider using backup copy jobs without WAN Acceleration. However, if you use WAN accelerators in that scenario, it may require deployment of multiple WAN accelerator to fully saturate the WAN link.

[^1]: A pair of WAN accelerators means any source WAN accelerator paired with the target WAN accelerator.
[^2]: All Linux operating systems are considered as one in terms of WAN accelerator sizing.
