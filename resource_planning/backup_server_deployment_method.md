# Deployment Method
You may deploy the Veeam Backup & Replication server as either a physical or virtual server. It will run on any server with Windows Server 2008 R2 or higher installed (64-bit only). Install Veeam Backup & Replication and its components on dedicated machines. Backup infrastructure component roles can be co-installed. The following guidelines may help in deciding which deployment type is the best fit for your environment.

## Virtual deployment
For most cases, virtual is the recommended deployment. As it provides high availability for the backup server component via features like vSphere High Availability, vSphere Fault Tolerance or Hyper-V Failover Clustering. It also provides great flexibility in sizing and scaling as the environment grows.

The VM can also be replicated to a secondary location such as a DR site. If the virtual machine itself should fail or in the event of a datacenter/infrastructure failure, the replicated VM can be powered on. Best practice in a two-site environment is to install the Backup server in the DR site, in the event of a disaster it is already available to start the recovery.

## Physical deployment
In small-medium environments (up to 500 VMs) it is common to see an all-in-one physical server running the Backup & Replication server, backup proxy and backup repository components. This is also referred to as an "Appliance Model" deployment.

In large environments (over 2,500 VMs) installing Backup & Replication services on separate servers either virtual or physical will provide better performance. When running many jobs simultaneously, _consuming large amounts of CPU and RAM,_ scaling up the virtual Backup & Replication server to satisfy the system requirements may become impractical.

An advantage of running the Veeam Backup & Replication server on a physical server is that it runs independently from the virtual platform. This might be an ideal situation when recovering the virtual platform from a disaster. Should the physical server itself fail, there are additional steps to take before reestablishing operations:

  1. Install and update the operating system on a new server
  2. Install Veeam Backup & Replication
  3. Restore the configuration backup

In an enterprise environment, you may choose to install an additional backup server to speed up the recovery process during a disaster. You may re-use existing availability components such as a proxy or repository server for the standby Backup & Replication server. During a disaster the configuration backup can easily be restored to this server.

__Tip:__ It is recommended to store the configuration backup, _using a file copy job_, in a location that is always available to this standby Backup & Replication server.
