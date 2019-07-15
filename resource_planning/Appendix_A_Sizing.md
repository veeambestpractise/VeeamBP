## Sizing and System Requirements Appendix


This appendix is a cumulative section on base sizing metrics, there is much more to sizing a Veeam Infrastructure and performing to the highest level. These figures here are guidelines to follow as a starting point. Each section is in much more detail in its relative chapter in the guide, please read each section first and you will gain an insight as to why these numbers are recommended.

Sizing with Veeam is cumulative in respect to configurations, if you want to create an all-in-one appliance (Appliance Model) add all the resource requirements together (CPU + Memory) to understand what in total you will need, the same goes if you only wish to have proxy and repository in one host.

Please also bear in mind that these figures reflect Veeam’s resource requirement, you must take the hosts system requirements into your calculation, this will depend on what you are using which is why we have not detailed it here.

#### Veeam Backup and Replication management server resources.

Recommended Veeam backup server resource configuration is:

##### Minimum Resources
* The minimum Compute is 2 CPU cores.
* Minimum memory, 8 GB RAM.
* Minimum HDD space is 60GB (inclusive of Logs, vPowerNFS, VBR software)
Recommendations for sizing.
* 1 CPU core (physical or virtual) and 4 GB RAM per 10 concurrently running jobs.
* For per job backup files: 30 VMs per job
* For per VM backup files: 300 VMs per job
* Base HDD is 40GB for software install location
* Plan for 3 GB log file space per 100 virtual machines, with a 24 hour RPO
* vPowerNFS location with reserve capacity of 10GB (100GB per TB of space if you plan to do many recoveries or planning SureBackup tests running many vm’s at the same time)
* Extra space for guest indexing processing a windows host: 100MB per 1Million files (temp file space)
* Extra space for guest indexing processing a Linux host: 50MB per 1Million files (temp file space)
* Storage space for Guest indexing before Enterprise manager flush: 2MB per 1 million files (compressed)


 
#### Proxy Server Resources

When sizing a proxy server remember, the ability to execute a task on the proxy will be affected by the repositories ability to process all the tasks from the proxies in infrastructure. If a repository has 20 cores, then the maximum processed tasks will be no more than 20 tasks from any proxy or group of proxies in the backend fabric of Veeam.

Recommended Veeam Proxy Servers configurations is:

* 1 CPU core per task (a task is a virtual hard drive)
* 2GB RAM per task
* Minimum of 500MB of HDD working space per task

This is based on a rounded figure offering approximately 30 VMs in a single backup job which will finish around an 8 hours backup window if in a per job backup, if a per VM repository is used more can be added. Please read the sizing and repository section for a full detailed description of parallelization of workloads in a Proxy.


#### Repository Server Resources

This is not about sizing for capacity of your repository but the resources required to accommodate the workloads form backups and restores.

When sizing a repository server remember, the ability to execute a task on the repository will be affected by the proxy’s ability to process all the tasks from the proxy’s. If a repository has 20 cores, then the maximum processed tasks will be no more than 20 tasks from any proxy or group of proxies in the backend fabric of Veeam to that repository.

Recommended Veeam Repository Server configurations is:

* 1 core per task
* 4GB per task
* Hard drive space is calculated based off retention points, type of backup used (full, Incremental, synthetic, forever forward incremental or reverse incremental.)

There is a much more detailed section in the guide.

 
#### SQL Server Database Sizing Guide

Veeam Backup & Replication may consume high amounts of CPU and RAM while processing backup or replication jobs. To achieve better performance and load balancing it is necessary to provide sufficient RAM and CPU resources.
If possible, follow these guidelines:

Concurrent Jobs  | CPUs |Memory
------------| -----------|---------
Up to 25	|	2CPUs |4GB RAM
Up to 50	| 4CPUs	| 8GB RAM
Up to 100 |	8CPUs |	16GB RAM


**Note:** Concurrently running jobs include any job type with a continuous schedule such as Backup Copy Jobs.
When running more than 100 jobs concurrently increase compute resources in line with the table above to meet the resource need of the workload.
Veeam installation package includes SQL server 2012 Express Edition, the basic limitations of this software are as follows:
*	Each instance uses only up to 1 GB of RAM
*	Each instance uses only up to 4 cores of the first CPU
*	Database size cannot exceed 10 GB

If any of the below apply consider using SQL standard or Enterprise editions
*	When protecting more than 500 VMs
*	When using Files to Tape jobs extensively
*	When unable to configure an external staging server
*	When databases are using advanced features of Microsoft SQL Server
