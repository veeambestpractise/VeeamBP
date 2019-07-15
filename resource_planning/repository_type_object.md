# Object Storage Repository

The Object Storage Repository cannot be used on its own but has to be configured as [Capacity Tier](./repository_sobr_capacity_tier.md) in the [Scale-out Backup Repository](./repository_sobr.md).

## Lifecycle Rules & Tiering
Do **not configure any tiering or lifecycle rules** on object storage buckets used for Veeam Object Storage Repositories. This is currently **not supported**.

The cause for this is:

1. Tiering and lifecycle rules in object storages are based on object age. However, with Veeam's implementation even a very old block could still be relevant for the latest offloaded backup file when the block was not changed between the restore points. An object storage vendor can not know which blocks are still relevant and which not and thus can not make proper tiering decisions.
2. The vendor APIs for the different storage products are not transparent. E.g.  accessing Amazon S3 or Amazon Glacier requires the use of different APIs. When tiering/lifecycle management is done on cloud provider side Veeam is not aware of what happened and cannot know how to access which blocks.

## Manual Deletion
Do **not delete manually** from an object storage bucket used for a Veeam Object Repository. Veeam will take care of deleting old objects based on your configured retention period in the backup or backup copy job.

You can safely delete everything manually when the Object Storage Repository is  decomissioned completely (unconfigured in VBR).

## Security
Create an own bucket and own user where possible for the Object Storage Repository and limit the user account to have only the required access on the object storage bucket.

## Cost Considerations
When using public cloud object storage always consider all costs. 

Putting data to the object storage requires API PUT calls. These calls normally cost by the thousand.

When data is at rest the used resources are normally priced by GB/month.

Do never forget prices for restores. These prices do include API requests (GET) but also the egress traffic cost from the cloud datacenter which can be immense depending on how much data is required to be pulled from the cloud.
Veeam tries to leverage the locally available data blocks to reduce cost, but blocks which are not present on premise have to be pulled from the cloud.