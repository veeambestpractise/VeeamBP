<!--- This was last Changed 03-05-17 by PS --->
# Tape Support

## Overview

The diagram below illustrates the main components and processes within
the backup infrastructure when tape support is implemented in Veeam
Backup & Replication:

![](../media/image25.png)



## Tape Device Connection

#### The following configuration prerequisites must be met:

- All connection types require driver installation
-	You can use generic drivers from Microsoft Windows, but they may not provide as high performance as the vendor’s
-	Separate drivers for tape drives and for tape media libraries should be installed
-	StorageTek ACSLS is not supported while a direct connection to the library is needed
-	Dynamic Drive Sharing is not supported
-	Library Partitioning is supported
-	Multiple control paths are supported only when control path failover and MPIO is configured correctly. Please contact the vendor for more information.

#### Connection Type Compatibility

- FC/SAS/SCSI/FCoE/Infiniband/iSCSI or other block technology to physical Tape Proxy are supported with Windows driver as long as the tape vendor supports the connection. (“Unknown media changer” support for FC/SAS and VTLs)
- FC/SAS redirect to VMware VM is unsupported
- FC/SAS redirect to Hyper-V VM	is unsupported
- FC/SAS to iSCSI Converter/Bridge is supported
- Starwind Tape Redirector is supported

#### Tape device support
The Veeam Ready database provides a list of all partner solutions that have successfully passed Veeam’s testing criteria. Solutions are grouped by company name, Veeam Ready classification, and more. [Veeam Ready Database](https://www.veeam.com/ready.html)

#### Supported
- LTO-3 or higher
- For VTLs, see the corresponding section under Deduplication Storage

#### Not supported
- IBM "Jaguar" TS11x0 Enterprise tape drives
- StorageTek T10000 tape drives
- Older Tape drives like DLT or AIT

#### Drivers
-	IBM drivers: use “non-exclusive” driver setup and start installation with administrative rights.
-	HP drivers: these are not installable with the downloaded install .exe file on a VM (for example, to use with VTL). As a solution, run the install .exe and choose Extract. Use Device Manager –> Update driver and select the drivers for tape drives and (if you use HP/HP emulation tape library) for media changer.


#### Unknown Medium Changers

Veeam supports medium changers that have no Microsoft Windows drivers available. Make sure that such device is recognized as an unknown medium changer in the Microsoft Device Manager list.

It is recommended that you use tape devices with original equipment manufacturer (OEM) drivers. Limitations VMware does not support tape drives connected directly to ESX(i) 4.x and later. For more information, see VMware vSphere Release Notes.  

For more details and recommendations on configuring vendor-supported tape drives and media changers on ESX/ESXi, refer to VMware documentation at https://kb.vmware.com/s/article/1016407.


**Note**:  Veeam Backup & Replication uses the MTF (Microsoft Tape Format) industry format to write data to tape. Veeam Backup & Replication also supports using WORM (Write Once Read Many) tapes.
 
