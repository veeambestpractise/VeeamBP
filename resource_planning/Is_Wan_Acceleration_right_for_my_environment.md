<!--- This was last Changed 03-05-17 by PS --->
## Is Wan Acceleration right for your environment?

Wan Acceleration is designed to optimize high latency or low bandwidth links between locations. there is a natural overhead and resource requirement when this is in operation and there will come a break point in regard to does Wan Acceleration work for me.

There are a number of ways to determine this based around speed and your available resources.

Wan Acceleration can be one to one or one to many connections, the first thing you should consider is the bandwidth available between the locations to see if the cost of optimizing your traffic is outweighed by the speed of your link.


The following is a general rule to look at when designing your transport:

### Global Cache on Spinning Disk

- **Link less than 3Mb/s** - WAN likely saturated; processing rate dependent on data reduction ratio (estimated 10x)
- **Link more than 3Mb/s and  less than 50Mb/s** - WAN will not be fully utilized, expect ~5MB/s processing rate but less bandwidth.
- **Link more than 50Mb/s** - WAN will not be fully utilized, using direct mode copy will use more bandwidth but likely be faster**

These numbers are to be considered as a base line , “Your mileage may vary”. The performance of the underlying storage where the Global Dedupe Cache is located can greatly impact the performance of the WAN Accelerator function.
 
Tests show that there are no significant performance differences in using spinning disk drives as storage for the target WAN accelerator cache rather than flash storage. However, when multiple source WAN accelerators are connected to a single target WAN accelerator (many-to-one deployment), it is recommended to use SSD or equivalent storage for the target cache, as the I/O is now the sum of all the difference sources.

One more point to focus on is the repository used at the target-wan-accelerator, data may be taken from the repository at the target WAN accelerator if the data is not found in the global cache but is known to exist in a previous transfer. If slow disks are used it can have an impact on the speed of the completion of the job and overall processing rate.

Other factors are also present such as is this link going to have bi-directional data flow when using the Wan Accelerators, how many jobs will be using the link at the same time. Measure your overall saturation of the link prior to using Wan Acceleration to ensure that it meets your needs.
