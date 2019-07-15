# IBM Spectrum Virtualize storage

Make sure that a license for the IBM Spectrum Virtualize storage system supports IBM FlashCopy

## Backup from IBM Spectrum Virtualize secondary storage array

With IBM Spectrum Virtualize, the main requirement is that Hyperswap function is configured between the two arrays. This allows volumes to maintain a synchronous copy of themselves on the other array, which is the main difference compared to other storage systems. The replicated volumes are exported in a read-only mode and thus act as passive volumes. In such a configuration, both arrays are active and hold primary production volumes and secondary volumes. Note that we can back up or replicate VM data from both arrays

When Veeam Backup & Replication is configured to use snapshots of secondary volumes, the storage snapshot is triggered directly on the secondary volume, which means that the primary one remains untouched from a backup activity perspective.

## Configuring Veeam Backup & Replication

Unlike many other features, this one isn’t configured in the GUI as it is usually. Enabling it is controlled through the Windows Registry on the machine hosting the Veeam Backup Server role. A new registry key needs to be created using the following parameters:

Location: HKEY_LOCAL_MACHINE\SOFTWARE\Veeam\Veeam Backup and Replication\
Name: IbmHyperSwapUseSecondary
Type: REG_DWORD (0 False, 1 True)
Default value: 0 (disabled)
Description: controls whether Veeam will use volume from secondary site to backup from
To enable the feature, the value must be set to 1. For the new setting to be effective, you need to restart the Veeam Backup Service manually.

