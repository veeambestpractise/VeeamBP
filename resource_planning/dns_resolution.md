# DNS Resolution

Domain Name System (DNS) resolution is critical for Veeam Backup & Replication deployment (VBR)
and configuration. All infrastructure components should be resolvable through a fully qualified domain name (FQDN). This is especially important for vSphere/Hyper-V hosts and clusters. Resolvable means that components are accessible through both forward (A) and reverse (PTR) lookups.

Ensure that the Veeam Backup & Replication server is installed on a machine that has a resolvable fully qualified domain name (FQDN). To check that the FQDN is resolvable, type `nslookup your-vbr-server-fqdn.domain.local` at a command line prompt. If the FQDN is resolvable, the nslookup command returns the IP and name of the Veeam Backup & Replication server.

Only if DNS resolution is __not__ available you may add the infrastructure components like e.g. VMware vCenter, ESXi and managed Veeam servers to the local `hosts` file on _all_ managed Veeam servers. When using this workaround it is recommended to add both short name and fully qualified domain name in the `hosts` file.

When ESXi hosts are added to vCenter it is recommended to use FQDN. When backing up through the network with the Network Block Device (NBD) transport mode, the FQDN is returned via VMware API for Data Protection (VADP) so the backup proxy server must be able to resolve the FQDN via DNS. Using the `hosts` file the data transport path can be altered for NBD transfers.

Please see the example below.

## Example `hosts` file

	10.0.4.10	vcenter	vcenter.example.com

	# 10.0.4.21	esx1	esx1.example.com # commented out management interface
	# 10.0.4.22	esx2	esx2.example.com # commented out management interface

	10.255.4.21	esx1	esx1.example.com # dedicated 10 GbE backup network
	10.255.4.22	esx2	esx2.example.com # dedicated 10 GbE backup network

To explicitly alter the data transport path, the `hosts` file must be deployed on all backup proxy servers. For easier management, please see the [Carbon module](http://get-carbon.org) and [`Set-HostsEntry`](http://get-carbon.org/Set-HostsEntry.html) by Aaron Jensen.
