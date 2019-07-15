# Capacity Tier

The Capacity Tier extends the SOBR virtually unlimited depending on the type of object storage which backs the Capacity Tier. 

Only one Capacity Tier can be configured per SOBR. The Capacity Tier must be an [Object Storage Repository](./repository_type_object.md).

To understand more about the Capacity Tier and how offloading works, please refer to the Veeam Helpcenter article about [Capacity Tier](https://helpcenter.veeam.com/docs/backup/vsphere/capacity_tier.html?ver=95u4).

## General

The VBR 9.5 U4 implementation of Capacity Tier is a **move only** functionality. This means within a SOBR the backup files do only exist once, either on a Performance or on the Capacity Tier extent. Therefore the Cloud Tier offload functionality is not a replacement for a backup copy and is no proper way of fulfilling the 3-2-1 rule.

The retention of the objects in the Capacity Tier is controlled by the backup or backup copy job's retention policy in restore points and not on repository level.
The operational restore window in the SOBR configuration does only define which retention files can be offloaded.

Offloading to object storage will only happen if the retention period and the operational restore window do overlap. E.g. if you configure 14 retention points with one backup per day and you want to offload to the Capacity Tier after 14 days, you will never offload anything. If you configure 21 retention points with the same operational restore window there should be roughly 7 retention points offloaded to object storage (based on other requirements, like sealed backup chains).

## Block Size
The created data-block-objects in the object storage are based on the backup's configured block size (Storage optimizations). The default is `Local Target` and refers to an uncompressed block size of 1024 KB. Every block is offloaded as a single object in the object storage and thus requires one API call per read or write operation (GET/PUT).

For the same amount of data a larger block size would mean less objects and less API calls, on the other hand larger block sizes mean a higher probability of changes in the block which reduces the efficiency of intelligent block cloning.

Experience shows that the default `Local Target` setting with the uncompressed 1024 KB block size is the best general purpose setting and should be configured in most cases. In corner cases other block sizes might show lower cost, e.g. by reducing API calls.