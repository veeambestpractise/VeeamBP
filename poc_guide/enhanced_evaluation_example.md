# Enhanced Evaluation - Workshop Example

This section describes how to conduct an infrastructure discovery and assessment session with a customer. Below is an example of how Veeam Architects hold such meetings with customers. The example below is just one example of many possible ways of the meeting content; please have a look at other chapters of this guide to prepare for such meeting.

## Infrastructure Discovery
1.	Start with the first main customer datacenter. Figure out the following:
  1.	Virtualization platform and version
  2.	Main storage system, type, connection
  3.	Is storage virtualization used (between the storage arrays and hypervisor)?

2.	Next would be the second customer datacenter (if available)
  1. Is this the same platform as the main datacenter, if not what is it?
  2. Are there any storage replication/mirroring involved?
  3. Is an Active/Active cluster used?

    For proper backup proxy implementation and backup mode selection, it is important to know where the data that you want to back up is located, and whether you can access all data from a single site.

3.	Obtain information about network connections:
  1.	Is there a 10 GbE LAN?
  2.	Is there a WAN connection between the 2 datacenters?
  3.	What is the VMKernel Interface physical link speed?
  4.	Is the VMware vCenter Server or Microsoft SCVMM server physical or virtual? Where is it located? Are both hypervisor platforms used?

  This is necessary to know if you plan to use the Virtual Appliance (HotAdd) or Network backup mode.
  10GbE gives you faster processing for the Network mode. To learn more, see the [Backup Proxy](../resource_planning/proxy_server_and_transport_modes.md) chapter.

4.	Define the amount of production data:
  1. Number of VMs (needed to design jobs)
  2. Used data (needed to define the backup target and configure jobs settings)
  3. Number of ESXi hosts and number of used sockets (this regards Veeam licensing).
  4. Number of clusters
  5. Other information

5.	Create the first Veeam implementation draft/sample scenario:

  1. Start with the repository, discussing customer demands. In the example, customer wanted to have the backup data in both data centers. If so, you could decide to implement repositories on both sides (half of the data on each side) and use the backup copy job to move data to the second site.  
  2. Discuss proxy implementation. The customer agreed to implement physical proxy servers connected to their Fibre Channel network. As the customer used thick-provisioned VMware VM disks, this ensured a fast and reliable backup and restore. Check out the [Backup Proxy](../resource_planning/proxy_server_and_transport_modes.md) section of this guide to determine the best proxy implementation and select a transport mode for the environment.
  3. Plan for the backup server.
  In this example, it was placed on a VM and replicated to the second datacenter. (The underlying datastore of the VM was not replicated to the second site, only the VM.)
  4. Add other required components.
  The customer was already using two IBM TS3500 libraries for long-term retention with the existing backup software (agents). They prepared a partition on each library with 4x LTO6 drives for use with Veeam. You would proceed and connect them to the 2 physical servers (having the proxy and repository roles assigned), and additionally assign the tape server role to these servers.

6.	Define OS/applications:
  1. Create a list of used operating systems.
  2. Create a list of all applications starting with the most critical.
Find out whether Microsoft SQL and Microsoft SharePoint are used, as it can influence the version and type of the Microsoft SQL Server on which the Veeam configuration database must be deployed (Express Edition may be not sufficient).

7.	Define business-critical applications/VMs to plan for availability.
Planning for backup is very important for them, as this mainly influence the RPO and stability of existing applications. It is even more important to plan for disaster recovery scenarios.
  1. Define the number of VMs that are business critical.
  2. Find out whether slower performance is OK at disaster recovery (consider using Instant VM Recovery).

In this example, the customer used a third small datacenter with a single storage system (Quorum) for the storage virtualization. During the discussion the customer identified 50 VMs that were business-critical and needed full performance even at disaster recovery. Thus, in the next step, you would add 2 ESXi hosts to that Quorum datacenter and replicate these 50 VMs every hour to that datacenter. The connection speed is to be 10 GbE. So, in case of disaster recovery the customer could just boot up all VMs with full speed.

**Important!** use all available Veeam possibilities to implement the best RTO and RPO times in a customers environment.

For the VM recovery scenario, you can mix classic VM restore (best for small VMs), Instant VM Recovery (best for huge data servers) and VM replica failover (best for database systems with extreme I/O requirements).
Together with the customer, check the “possible failure domains” (single storage system / whole datacenter / 1 datastore) and decide if the designed Veeam implementation fits into these needs and is in line with the budget.

## Network and Firewall

Veeam Availability Suite is elastic and lets you implement different backup infrastructure schemes. Firewalls can be used between all backup infrastructure components. The only exception is RPC inspection functionality: it can cause delays in connections, and Veeam Backup & Replication can run into timeouts.
However, the best practice is to place backup infrastructure components in the same network segment as the corresponding VMware components to allow for efficient and fast usage of the network bandwidth.

## Proxy/Repository Systems

Proxy and repository servers should be placed in the VMKernel networks. Veeam Backup & Replication uses the VMKernel interfaces to read out configuration data and disk data (in case of Network mode), and to map Veeam vPower NFS data stores for fast recovery (Instant VM Recovery).

## Backup & Replication Server

As the backup server communicates mainly with the vCenter Server and other backup infrastructure components, it should be placed next to the vCenter Server in most cases.
The backup infrastructure for this sample scenario would look as follows:
![Enhanced Evaluation - Example](../media/image48.png)

## Veeam ONE

Veeam ONE components should be placed next to the vCenter Server and should be able to read from the backup server and ESXi hosts (over the CIM protocol) as well. See Veeam ONE documentation for more information: [Veeam ONE Deployment Guide](https://helpcenter.veeam.com/docs/one/deployment/about.html?ver=95).

## Enterprise Manager

When Veeam Backup Enterprise Manager is used with Self-Restore services, it should be placed in the internal DMZ in most cases.

## Restore Points

In the sample case, the customer needed daily backup with 14 restore points; the points were to be held on 2 sites (multiplied with backup copy job). The customer also wanted to offload the weekly full backups on tape and hold them for a period slightly longer than one year in both tape libraries.

The customer also needed to replicate the most critical VMs to the Quorum datacenter hourly, between 7:00 and 19:00. The number of replication restore points to be maintained was the maximum possible (here 28 restore points).

In many architecture meetings, planning for the retention policies is the most time-consuming part as you are likely to engage different administrators and management team members from different departments in this process. These team members have to translate their file-based existing restore point policies into a new way (image-level backup). It is a matter of concern because a longer retention chain will result in expensive storage space costs.

**Important!** Remember to agree on backing up Microsoft SQL Server transaction logs with Veeam Backup & Replication.

If speaking about the storage sizing, the tool at [Veeam Restore Points Calculator](http://rps.dewin.me/) can help to illustrate the retention chains on disk and estimate the required capacity.
