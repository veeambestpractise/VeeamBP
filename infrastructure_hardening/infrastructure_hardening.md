# Infrastructure Hardening
Running your Veeam Backup & Replication infrastructure in a secure configuration is a daunting task even for security professionals. This chapter provides practical advice to help administrators to harden their infrastructure following security best practices so that they can confidently deploy their Veeam services and lower their chances of being compromised.

Hardening is about securing the infrastructure against attacks, by reducing its attack surface and thus eliminating as many risks as possible. One of the main measures in hardening is removing all non-essential software programs and utilities from the deployed Veeam components. While these components may offer useful features to the administrator, if they provide ‘back-door’ access to the system, they must be removed during the hardening process.

But also, creating visibility in what goes on in the infrastructure is part of hardening your infrastructure. Making sure you will notice when an attack is/or has taken place and then making sure logs and traces are saved for law-enforcement and security specialists when needed.

## Protect
Protecting your infrastructure successfully is all about understanding the current attack vectors; what and whom you are protecting, your Veeam infrastructure, against. If you know what and whom you are protecting against, makes it easier to take the correct countermeasures. One of those countermeasures is hardening.

Looking at the different Veeam Backup & Replication components you have to protect the following components:
* Veeam Backup server
* User Accounts
* Backup repositories
* Backup data flows

Consider the Veeam Backup & Replication server to be the **Number 1** target on your infrastructure and it should have very restricted access. As a general rule the backup server is the single greatest target a hacker can claim on your network. Also the backup repositories which holds the backup files are a primary target.

## Hardening
Within the hardening process of your Veeam infrastructure there are a few steps everyone should always consider and act upon, namely:


1. [Secure by Design](#secure-by-design)

2. [Remove Unused Components](#remove-unused-components)

3. [Console Access](#console-access)

4. [Roles and Users](#roles-and-users)

5. [Required Permissions](#required-permissions)

6. [Encryption](#encryption)

7. [Backup & Replication Database](#backup-&-replication-database)

8. [Segmentation](#segmentation)

9. [Visibility](#visibility)

10. [Recovery Strategy](#recovery-strategy)



## Secure by Design
Overly complex designs become harder for the IT team to manage and overlook and it makes it easier for an attacker to exploit and stay in the shadows. Simpler designs that can be easily overviewed are in basis more secure. Use the K.I.S.S.[^1] (Keep It Simple and Straightforward) principle for your designs.

Adding security to an already existing infrastructure is much harder and costly than thinking about it while designing a new or refreshing an existing infrastructure. In a virtual infrastructure, it is good use to build up a Master image which has been hardened from the start. Removing all known attack vectors and only open up access when Veeam components are added and needs specific (port) openings or extra software to function properly. This way all builds are consistent and kept up-to-date which makes it secure in the basis.

Consider the Veeam Backup & Replication server to be the **Number 1** target on your infrastructure and it should have very restricted access. As a general rule the backup server is the single greatest target a hacker can claim on your network.

## Remove Unused Components
Remove all non-essential software programs and utilities from the deployed Veeam components. While these programs may offer useful features to the administrator, if they provide ‘back-door’ access to the system, they must be removed during the hardening process. Think about additional software like **web browsers**, **java**, **adobe reader** and such. All parts which do not belong to the operating system or to active Veeam components, remove it. It will make maintaining an up-to-date patch level much easier.


**Veeam Backup & Replication Server**
* Remove the Backup & Replication Console from the Veeam Backup & Replication server. The console is installed locally on the backup server by default.
* Switch off the Veeam vPower NFS Service if you do not plan on using the following Veeam features: SureBackup, Instant Recovery, or Other-OS File Level Recovery (FLR) operations.

### How to remove the Veeam Backup & Replication Console
The Console can not be removed through the installer or by using Add/Remove in Windows.
Open a `cmd` prompt with administrative access. On the command prompt type: `wmic product list brief > installed.txt` this will create a text document with all installed products and their respective Product Codes.

For uninstalling Veeam Backup & Replication Console, first de-install all Veeam Explorers:
* Veeam Explorer for Microsoft Exchange
* Veeam Explorer for Microsoft Sharepoint
* Veeam Explorer for Microsoft Active Directory
* Veeam Explorer for Microsoft SQL
* Veeam Explorer for Oracle

You can uninstall these components by using: `msiexec /x {ProductCode}`

Example for uninstalling the Veeam Backup & Replication console is: `msiexec /x {D0BCF408-A05D-45AA-A982-5ACC74ADFD8A}`

**Enterprise Manager**

When Enterprise Manager is not in use de-install it and remove it from your environment.


## Console Access
The Veeam Backup & Replication console is a client-side component that provides access to the backup server. The console lets several backup operators and admins log in to Veeam Backup & Replication simultaneous and perform all kind of data protection and disaster recovery operations as if you work on the backup server.

Install the Veeam Backup & Replication console on a central management server that is, positioned in a DMZ and protected with 2-factor authentication. Do NOT install the console on the local desktops of backup & recovery admins.

## Roles and Users
Deploy an Access Control policy, managing access to management components is crucial for a good protection. Use the _**principle of least privilege**_. Provide the minimal privilege needed for some operation to occur.
An attacker who gained high-privilege access to backup infrastructure servers can get credentials of user accounts and compromise other systems in your environment. Make sure that all accounts have a specific role and that they are added to that specific group.

Containment to keep the attackers from moving around too easily. Some standard measures and policies are:
* Do not use user accounts for admin access, reducing incidents and accidents
* Give every Veeam admin his own admin account or add their admin account to the appropriate security group within Veeam, for traceability and easy adding and removal
* Only give out access to what is needed for the job
* Limit users who can log in using Remote Desktop and/or Veeam Backup Console
* Add 2-factor authentication to highly valuable assets
* Monitor your accounts for suspicious activity

A role assigned to the user defines the user activity scope: what operations in Veeam Backup & Replication the user can perform. Role security settings affect the following [operations](
https://helpcenter.veeam.com/docs/backup/vsphere/users_roles.html?ver=95)

### Password management policy
Use a clever Password management policy, which works for your organization. Enforcing the use of strong passwords across your infrastructure is a valuable control. It’s more challenging for attackers to guess passwords/crack hashes to gain unauthorized access to critical systems.

Selecting passwords of 10 characters with a mixture of upper and lowercase letters, numbers and special characters is a good start for user accounts.

For Admin accounts adding 2-factor authentication is also a must to secure the infrastructure.

And for service accounts use 25+ characters combined with a password tool for easier management. An Admin can copy and paste the password when needed, increasing security of the service accounts.

### Lockout policy
Use a Lockout policy that complements a clever password management policy. Accounts will be locked after a small number of incorrect attempts. This can stop password guessing attacks dead in the water. But be careful that this can also lock everyone out of the backup & replication system for a period! For service accounts, sometimes it is better just to raise alarms fast. Instead of locking the accounts. This way you gain visibility into suspicious behavior towards your data/infrastructure.


## Required Permissions
Use the _**principle of least privilege**_. Provide the minimal required permissions needed for the accounts to run. The accounts used for installing and using Veeam Backup & Replication must have the following [permissions](
https://helpcenter.veeam.com/docs/backup/vsphere/required_permissions.html?ver=95).

If VMware vCenter Server is added to the backup infrastructure, an account that has administrator permissions is required. Instead of granting administrator permissions to the account, you can configure more granular permissions. Veeam has identified the minimum permissions required for the various software functions. Review the ["Required Permissions" document](https://www.veeam.com/veeam_backup_9_0_permissions_pg.pdf) (not changed since V9.0) and configure the accounts used by Veeam Backup & Replication to meet these requirements.

Particularly, backup proxies must be considered the target for compromise. During backup, proxies obtain from the backup server credentials required to access virtual infrastructure servers. A person having administrator privileges on a backup proxy can intercept the credentials and use them to access the virtual infrastructure.

### Patching and Updates
Patch operating systems, software, and firmware on Veeam components. Most hacks succeed because there is already vulnerable software in use which is not up-to-date with current patch levels. So make sure all software and hardware where Veeam components are running are up-to-date. One of the most possible causes of a credential theft are missing guest OS updates and use of outdated authentication protocols. To mitigate risks, follow these guidelines:

* **Ensure timely guest OS updates on backup infrastructure servers**. Install the latest updates and patches on backup infrastructure servers to minimize the risk of exploiting guest OS vulnerabilities by attackers.

* **Choose strong encryption algorithms for SSH**. To communicate with Linux servers deployed as part of the backup infrastructure, Veeam Backup & Replication uses SSH. Make sure that for the SSH tunnel you use a strong and proven encryption algorithm, with sufficient key length. Ensure that private keys are kept in a highly secure place, and cannot be uncovered by a 3rd party.

## Encryption
Backup and replica data is a highly potential source of vulnerability. To secure data stored in backups and replicas, follow these guidelines:

* **Ensure physical security of target servers**. Check that only authorized personnel have access to the room where your target servers (backup repositories and hosts) reside.

* **Restrict user access to backups and replicas**. Check that only authorized users have permissions to access backups and replicas on target servers.

* **Encrypt data in backups**. Use Veeam Backup & Replication inbuilt encryption to protect data in backups. To guarantee security of data in backups, follow [Encryption Best Practices](https://helpcenter.veeam.com/docs/backup/vsphere/encryption_best_practices.html?ver=95).


Backup and replica data can be intercepted in-transit, when it is communicated from source to target over a network. To secure the communication channel for backup traffic, consider these guidelines:

* **Isolate backup traffic**. Use an isolated network to transport data between backup infrastructure components — backup server, backup proxies, repositories and so on. (also see segmentation)

* **Encrypt network traffic**. By default, Veeam Backup & Replication encrypts network traffic traveling between public networks. To ensure secure communication of sensitive data within the boundaries of the same network, you can also encrypt backup traffic in private networks. For details, see [Enabling Network Data Encryption](https://helpcenter.veeam.com/docs/backup/vsphere/enable_network_encryption.html?ver=95).

## Backup & Replication Database
The Backup & Replication configuration database stores credentials to connect to virtual servers and other systems in the backup & replication infrastructure. All passwords stored in the database are encrypted. However, a user with administrator privileges on the backup server can decrypt the passwords, which presents a potential threat.

To secure the Backup & Replication configuration database, follow these guidelines:

* **Restrict user access to the database**. Check that only authorized users can access the backup server and the server that hosts the Veeam Backup & Replication configuration database (if the database runs on a remote server).
* **Encrypt data in configuration backups**. Enable data encryption for configuration backup to secure sensitive data stored in the configuration database. For details, see [Creating Encrypted Configuration Backups](https://helpcenter.veeam.com/docs/backup/vsphere/config_backup_encrypted.html?ver=95).


## Segmentation
Add local protection mechanics, in addition to the border firewalls, intrusion detection, patching and such. You can make use of local mechanisms, like up-to-date anti-malware, firewalls and network segmentation. This way you create different rings-of-defense slowing an attacker down. A great way to strategically use segmentation is by implementing [Zones](./hardening-zones.md).

A good practice is to place the backup repositories in a special segment not accessible by any user. Like for instance the production storage is only available to the virtual infrastructure components and application servers. Not directly accessible by any user!

To segment your infrastructure and Veeam Backup & Replication components, make sure the firewalls on the local server installations have the correct [Ports](https://helpcenter.veeam.com/docs/backup/vsphere/used_ports.html?ver=95) opened.   

You can also deploy [VMware NSX](https://blogs.vmware.com/networkvirtualization/2016/06/micro-segmentation-defined-nsx-securing-anywhere.html/) as a counter measure with micro-segmentation to make sure the attack surface is as narrow as possible without blocking everyone to use the services. Visibility into the network and all data flows is crucial to help you protect all different rings/cells within your infrastructure. You can add the Veeam components to NSX policies to make sure they can communicate with each other without opening it up to any user.

### Ports
Try not to use obscure ports and other tricks to try and hide Veeam ports and protocols in use, while this may look like a good choice. In practice this often makes the infrastructure harder to manage which opens other possibilities for attackers. Obscurity is not security!


You can check which ports are in use by which service on a Windows system by using:

`netstat -bona > portlist.txt` you can open the text file with for instance `notepad portlist.txt`


## Visibility
To know when you are under attack or have been breached it is vital to have visibility in the whole data flow path. You should be able to know what is ‘normal behavior’ and what is NOT. Monitor your accounts and Veeam infrastructure for suspicious activity. Place virtual trip-wires, like e.g. creating a non-used admin account with alarms tied to it. When any activity on that account is observed, it will trigger a red alert instantly. There are several systems out there that can help you by alerting suspicious behavior so you get aware that someone is snooping around and is trying to gain access to your infrastructure. Visibility is Key!

It is important to get alerts as soon as possible while defending against other attacks like viruses, malware and ransomware. The biggest fear of these attacks is that they may propagate to other systems fast. Having visibility into for e.g. potential ransomware activity is a big deal.

Example Systems that could help you create visibility are:
* A system that detects possible ransomware activity is [Veeam ONE 9.5](https://www.veeam.com/wp-veeam-availability-suite-protection-against-ransomware-threats.html). There is a pre-defined alarm called “Possible ransomware activity.” This alarm will trigger if there is a high CPU utilization combined with lots of writes to disk.

* VMware vRealize Network Insight can take VMs, objects, groupings and their physical elements and easily fingerprint the application and determine the internal and external flows, the client connections, etc. this way you get an analysis of what is ‘normal’ behavior and what is not.

* VMware vCenter with alerts that are triggered on virtual trip-wires.


## Recovery Strategy
Have a recovery strategy in place, before you find out your infrastructure is breached you should know what to do when being compromised through attacks. Backup your data and make sure the backups cannot be accessed by an attacker to wipe them out. An offsite copy (air-gap) or read-only on any media is highly recommended to survive any attack.

### The 3-2-1-0 backup rule
The 3-2-1 rule is very general and it works for all data types (individual and corporate) and all environment types (physical and virtual). When backing up VMware or Hyper-V environments with Veeam, this rule becomes the [“3-2-1-0 backup rule”](https://www.veeam.com/blog/how-to-follow-the-3-2-1-backup-rule-with-veeam-backup-replication.html) where 0 means “0 errors” during the automatic recoverability verification of every backup with Veeam’s [SureBackup](resource_planning/vpower_nfs_and_virtual_lab.md).

Veeam Backup & Replication™ can help you to fulfill all 3-2-1-0 backup rule requirements.
* **Have at least three copies of data:** Setup Backup Jobs to create several backups for each of your VMware or Hyper-V VMs.

* **Store the copies on two different media:** Veeam is storage-agnostic, meaning it supports tapes, disks, the cloud and more. You can store your backups to any of the listed media.

* **Keep one backup copy offsite:** Setup Backup Copy Jobs to transfer your backup offsite faster with built-in WAN acceleration, or use Veeam Backup Cloud Edition to store your backups to one of 15 public clouds, including Windows Azure, Amazon Glacier, Google Cloud Storage and more.

### Educate your Staff
By deploying an employee awareness training you make sure that your employees are aware of strange behavior and of their critical roles in protecting the organization’s services and data. This is not only for the IT department, but for everyone within the organization, because every organization is becoming an IT company rapidly.


[^1]: KISS is an acronym for "Keep it simple, stupid" as a design principle noted by the U.S. Navy in 1960. The KISS principle states that most systems work best if they are kept simple rather than made complicated; therefore simplicity should be a key goal in design and unnecessary complexity should be avoided. A simple design is easier to overview and to secure as a whole. [Wikipedia](https://en.wikipedia.org/wiki/KISS_principle)
