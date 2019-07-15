<!--- This was last Changed 03-05-17 by PS --->
# Data Verification Using Virtual Labs

## Virtual Lab Appliance Overview

The Virtual Lab appliance operates as a gateway to offer network connectivity between the Veeam backup server and the isolated virtual machines in the Virtual Lab. It can also be used to provide access to other clients coming from the production network using static mapping. If VMs running in the isolated network need Internet access, the Virtual Lab appliance can act as a proxy server.

![](../media/image15.png)

When a SureBackup job is executed the static routes to reach the masqueraded networks are temporarily added to the routing table on the Veeam backup server. To review the routing table, you can open a command prompt on the Veeam backup server and execute:

`route print -4`

You may run this command before and after starting the SureBackup job to compare the differences.

The routes are added just after the Virtual Lab appliance has booted and has been correctly initialized by the Veeam backup server. As routes are added, this will ensure the Virtual Lab appliance is the gateway for all packets destined to the masquerade networks.

To avoid network reconfiguration of physical components, place the backup server and the Virtual Lab appliance in the same network subnet.

Check Veeam Backup & Replication documentation for configuration details:

- [vPower Users Guide](https://www.veeam.com/veeam_backup_9_0_evaluators_guide_vpower_vsphere_pg.pdf)

- [Recovery Verification help ](https://helpcenter.veeam.com/docs/backup/vsphere/recovery_verification_overview.html?ver=95)

## How SureBackup Job Works
SureBackup leverages the capabilities of the Virtual Lab appliance to create an isolated environment where different tests can be executed against VMs. These VMs are powered on directly from the backup files using the vPower technology.

### Booting the Virtual Lab Appliance
1.  Virtual Lab appliance configuration file is built and mapped to the Virtual Lab appliance as an ISO.

2.  Virtual Lab appliance network interfaces are reconfigured for appropriate isolated networks.

3.  The Virtual Lab appliance is powered on.

4.  The SureBackup job waits for IP configuration to be published and stabilized through VMware Tools.

5.  A static route for the configured masqueraded networks is added dynamically to the routing table of the Veeam backup server. Those static routes define the IP address of the Virtual Lab appliance as the gateway towards the masquerated networks.

### Booting Virtual Machines

1.  If the Application Group is based on backups,  Veeam publishes and registers VMs using Veeam vPower NFS from the repository containing the backup file. This step is skipped if the VMs are replicas.

2.  Veeam reconfigures the VMs and connects them to the isolated port groups of the Virtual Lab. If a network connection is configured to be connected to a port group that is not available in the Virtual Lab, those network are disconnected automatically.

3.  Veeam creates a snapshot for the VMs in order to redirect write operations to the production datastore selected during the Virtual Lab configuration and on which the virtual appliance files will be deployed.

4.  If the domain controller role is selected, registry settings are injected in the VM to ensure the NETLOGON service will not shutdown due to missing peer communication.[^1]

5.  VMs are powered on.

6.  During boot VMware Tools announce IP configuration of VMs. The SureBackup job waits for this information to stabilize.

**Note:** If VMware Tools are not installed on the virtual machine the job will wait for the duration of **Maximum allowed boot time** configured for the VMs. This will slow down SureBackup jobs significantly. Therefore, it is always recommended to install VMware
Tools on a verified VM.

###  Testing Virtual Machines

1. **VMware Tools heartbeat** is used for verifying that the VM OS is successfully started. SureBackup will wait a predefined amount of time for the heartbeat to register however if a heartbeat is seen before the timeout period expires the tests continue automatically.

2. **PING** tests are initiated according to the masqueraded network configuration. The ping is sent from the Veeam backup server using the static routes added during the job execution. Since the masquerade network is not part of the Veeam backup server's own subnet, the packet is sent to the gateway matching the Virtual Lab network (usually the virtual lab appliance).

3. **Application-specific testing** uses scripts and is enabled based on the roles assigned to a VM in the application group configuration. The built-in roles will check corresponding TCP ports for a given service. The built-in role for SQL Server provides additional testing (see next section), and custom scripts may be used for third party applications. Requests are sent from the Veeam backup server, and the routing to the virtual machine is handled by the Virtual Lab proxy appliance.

4. **CRC verification** is optionally available and is disabled by default. If enabled, it will ensure all content of the backup file is consistent with the hash values at the time they were written. This consistency check is using the CRC algorithm for hashing.

	**Note:** This feature reads the entire backup file, and requires significant time to complete.


5. **Custom scripts** are stored on the Veeam Backup Server and are launched by the account that controls the Veeam Backup Service. The authentication mecanism used to run remote commands on the tested guests will depend on the operating system.
	- **Windows script**: Veeam Backup & Replication starts a new shell (cmd.exe) as the user running the Veeam Backup & Replication Service (default being “Local System Account”) using the switch “/NETONLY” to use the specified credentials (e.g. database user in the tested environment) only when through a remote connection. This is imposed by the fact that the credentials needed for testing (specified in the credentials configuration tab) might not be existent in the domain where Veeam Backup Services are running.
	- **Linux scripts** will use a utility software called “plink.exe” to run remote commands over the virtual lab gateway. “plink. exe” is executed by the account running Veeam services while all subsequent commands in the script will use the credentials specified in the SureBackup script configuration tab.
	
6. **Specific concerns about SQL server authentication mode**: if the tested Microsoft SQL server accepts a Windows type authentication, the isolated domain credentials specified in the configuration tab will be used (like testing a SQL DB using the “runas /netonly” shell environment). If an SQL type authentication is requested by the tested database (typically “sa” user), the script should then be manually invoked and SQL credentials passed as arguments. The script to invoke is “%ProgramFiles%\Veeam\Backup and Replication\Backup\Veeam.Backup.SqlChecker.vbs” and arguments should be in the exact order:
- %log_path : default script log path “%programdata%\Veeam\Backup\Name_of_SureBackup_Job”
- %vm_ip% : masqueraded IP of the SQL server
- SQL user
- SQL password

	In this case the script will only use SQL type credentials making useless to specify Windows credentials as the script argument. 


If [Linked Jobs](https://helpcenter.veeam.com/docs/backup/vsphere/surebackup_job_joblink_vm.html?ver=95) are configured for the SureBackup job,
linked VMs will start booting once all virtual machines explicitly defined within the Application Group have been successfully booted
and verified. Remember that by default 3 VMs are tested at the same time in a Linked Job. There may be more than 3 VMs linked,
but the following ones will stay in the testing queue. The limit can be adjusted in the SureBackup job configuration wizard,
and may be increased if the backup repository and hypervisor can both handle the load accordingly.

### Guest predefined roles

When adding a guest image to the or the linked job, it is possible to assign a predefined role, for which Veeam Backup will automatically configure boot options and run a default set of application test accordingly, following rules described in below table.

|Role|Default startup options|Default test script|
|---|---|---|
|DNS Server|600s maximum boot time<br>120s application timeout|Connection test on port 53|
|Domain Controller (authoritative or non authoritative)|1800s maximum boot time<br>120s application timeout|Connection test on port 389|
|Global Catalog|1800s maximum boot time<br>120s application timeout|Connection test on port 3268|
|Mail Server|1800s maximum boot time<br>120s application timeout	Connection|test on port 25|
|SQL server|1800s maximum boot time<br>120s application timeout|Run “USE” SQL command against all defined databases on the server|
|Veeam Backup for Office 365|1800s maximum boot time<br>120s application timeout|Connection test on port 9191
|Web Server|600s maximum boot time<br>120s application timeout	Connection|test on port 80|

**Note :** You will notice that the Domain Controller startup mode (authoritative or not) can now be choosen. Veeam will mark the server accordingly so it boots in the selected mode. This is especially useful if many DC needs to be tested in a single SureBackup job. Please remind that if a single (or the first) Domain Controller is booted, it might use the authoritative mode. Subsequent Domain controllers must then use non-authoritative mode and will then synchronize from the authoritative one.

### Checking SQL Server Database Availability
A dedicated Visual Basic script is included to allow for testing whether all databases on a given instance are available. This script is available in the Veeam installation folder as the `Veeam.Backup.SqlChecker.vbs` file.

By default, the script tries to retrieve and check _all_ instances; you can optionally configure one or more specific instances to be tested. The script enumerates all databases and checks if these databases are available, using the `USE <db>`
statement.

When running scripts that require authentication, when executed the script will impersonate the service account under which the Veeam Backup Service is running (default is SYSTEM). To specify different credentials configure them in the 'Credentials' tab
in the Application Group settings.

![Credentials settings in Application Group](vpower_nfs_and_virtual_lab_1.png)

**Important!** To ensure successful authentication it is required for the specified user to have *public* access to all databases.

The `SqlChecker.vbs` script also accepts two additional parameters to use SQL authentication instead of Windows based authentication. In order to
use SQL authentication you need to add a custom test script instead of the built-in SQL Server role, and specify the following path and arguments:

* Name: SQL checker
* Path: _Browse for the `Veeam.Backup.SqlChecker.vbs` file_
* Arguments: `%log_path% %vm_ip% sa sa_account_password`

![Example custom role](../media/image16.png)

### Creating Custom Roles

Though there are a number of built-in tests intended for application-level testing, you may need to develop additional scripts for testing proprietary applications. This is the procedure to do so:

1.  Open the Veeam installation folder and look in the `SbRoles` folder. All roles are defined in the XML files available in this folder.

2.  To create custom roles, duplicate one of the above mentioned files and modify the `<Id>` tag using a UUID generator (such as     https://www.uuidgenerator.net). Use this configuration file to specify the GUI settings.

When creating custom roles for Linux-based applications you may need to execute the generated code locally within the VM. To do so, use `\Putty\plink.exe` shipped with the product and located in the Veeam Backup & Replication installation directory.

When executing bash scripts locally on a Linux virtual machine using `plink.exe`, the exit codes are passed to the SureBackup job, enabling correct error reporting. If using `plink.exe` in combination with a
SSH private key, you should connect manually (one time) to the VM via SSH using `putty.exe` from the Veeam backup server in order to accept the target VM SSH fingerprint; otherwise, the SureBackup job will wait for this input and ultimately timeout.

**Note:** You can use `puttygen.exe` to create a private key.

Another option for testing service availability with
`Veeam.Backup.ConnectionTester.exe` is described in
<https://www.veeam.com/kb1312>.

### Common Issues
When performing SureBackup, there are few common issues you may come across. Most of these issues are described
in Veeam knowledge base articles:

* When restoring Windows 2008 R2 virtual machines with the VMXNET3 network adapter,
  the resulting virtual machine obtains a new NIC, and all network settings have to be adjusted manually.
  The solution is explained in [Veeam KB1570](https://www.veeam.com/kb1570)

* When using DHCP with leases bound to MAC addresses, ensure that the vNIC MAC address is configured as `static`.
  Otherwise the VM will boot with a MAC in the Virtual Lab, and the VM may get a different IP address >
  [Setting a static MAC address for a virtual NIC](https://kb.vmware.com/s/article/219)

* Some Linux distributions use `udev` for assigning names to NICs. If the MAC address changes during
  replication or Instant VM Recovery, the NIC's configuration file may not be applied. For more
  information, please see [RHEL6 SureBackup](https://forums.veeam.com/vmware-vsphere-f24/rhel6-surebackup-t11681.html#p63750)

### Troubleshooting Mode

If you need to troubleshoot Virtual Lab, it is recommended to start sessions in the Troubleshooting Mode. To do so:

1.  Open up **Statistics** for a SureBackup job.

2.  Right-click the VM you want to troubleshoot.

3.  Select **Start**.

The SureBackup lab will now start in troubleshooting mode, which means that errors will not cause the Virtual Lab to shut down immediately.

If the selected VM is in an application group, this VM and previous ones are started. If the VM is part of a linked job, the entire Application Group and the selected VM is started.

This mode is especially helpful during an implementation phase while measuring application boot times via vPower NFS, or implementing custom verification scripts. When you have finished troubleshooting, you can stop the SureBackup session manually.

**Tip:** On the Virtual Lab appliance, ICMP traffic is blocked on all network interfaces connected to isolated networks, unless you check the "Allow proxy appliance to act as internet proxy for virtual machines in this lab". This may lead to undesired behavior of some systems, as they will be unable to ping their gateway.

## Virtual Lab in Complex Environments

When using standard vSwitches in a VMware vSphere infrastructure, the Virtual Lab proxy appliance and the isolated
networks must run on the same ESXi host ("Basic Single-Host" and "Advanced Single-Host" configurations).
The reason is that standard vSwitches and their port groups are bound to one single host. Since the Virtual
Lab port groups are isolated by nature, these networks are not known at the core network in terms of VLAN
tagging or routing.

When Distributed vSwitch (dvSwitch) is available, port groups can span multiple
ESXi hosts ("Advanced Multi-Host" configuration). Distributed vSwitches are typically
required when using Virtual Lab for replicas (SureReplica) as replicas will often span
multiple hosts. vSphere Distributed Resource Scheduler (DRS) may also distribute VMs
across multiple hosts within a cluster once they are started.

**Important!** Please check the following help article and the links at the
bottom of the webpage before you configure Virtual Labs for Distributed vSwitch:
[Advanced Multi-Host Virtual Labs](https://helpcenter.veeam.com/docs/backup/vsphere/surereplica_advanced_mutihost.html?ver=95).

Even in environments where Distributed vSwitch is available, make sure that the
Veeam backup server and the Virtual Lab proxy appliance are placed in the same
VLAN to prevent network packets (sent to the masquerading IP subnets) from being routed.

![](../media/image17.png)

Most DR datacenters are configured with different IP networks from production to allow for “active-active” configurations. In such cases, layer 3 (L3) is used for networking configuration and routing is in place to establish communications between the production site and the DR site.

For more information, please see the [Backup Server Placement](backup_server_placement.md)
section of this guide.

![](../media/image18.png)

[^1]: For more information about Domain Controller restore, please see the corresponding thread in Veeam
Community Forums > [Veeam B&R v5 recovery of a domain controller](https://forums.veeam.com/veeam-backup-replication-f2/veeam-b-r-v5-recovery-of-a-domain-controller-t7000-90.html)

## Scaling out SureBackup jobs

When it comes to managing thousands of virtual machines such as backup as a Service (BaaS) providers do, it might then become difficult to simply configure and run a SureBackup against a linked job containing thousands of images. Attention must then be paid to timing and resource consumption.

### Linked jobs
Using linked jobs A first option to scale out SureBackup jobs consists of leveraging the infrastructure resources at their maximum to test all the guests contained in the “linked job” attached to the job.

Here are a few guidelines to run the biggest possible SureBackup jobs:
* Leverage non-production infrastructure: As a very flexible feature, SureBackup allows to test the images on any cluster, this could be a small infrastructure dedicated to SureBackup, preproduction or development clusters usually underused at night.
* Run simple and quick tests: Commonly, backup providers don’t have administrative credentials on the objects they manage limiting or removing application testing from possible verifications. This simplifies the tests and reduces the time required to test the VMs using only the heartbeat test.
* Rely on fast read repository: SureBackup performance will heavily depend on the boot time of the tested guests. Keep in mind that Instant VM Recovery performance is directly related to underlying repository performance , especially on random reads. Another good option to apply to the repository is per-vm backup file since it will accelerate restore operations

### Using random guests in Virtual lab

Luca Dell’Oca raised the possibility in his blog post to daily randomly select a set of virtual machines while eliminating the ones already tested. These VMs are included in the Virtual Lab and then tested.
Assuming you could test 10 to 20 VMs daily, this can lead to 1000 VMs in 50 days.
You can also choose to make this even more simple and randomly select 10 VMs every day, giving a very good idea on possible backup corruption statistics while modifying the script.

**Note:** Per application group design the whole application group will fail when a guest test fails leaving further images untested. Also, all VMs of the application group will stay online until the application group is powered off, limiting by design the number of guests to simultaneously test.