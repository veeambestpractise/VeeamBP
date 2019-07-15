<!--- Last edited: Luca Dell'Oca on 03-05-2017 --->

# Encryption

## Overview

The encryption technology in Veeam Backup & Replication allows you to protect data both while it is in transfer between backup components and at rest, when it is stored at its final destination. This can be disk, tape or a cloud repository. Customers can use one of the encryption methods or a combination of both to protect against unauthorized access to important data through all the steps in the data protection process.

Veeam Backup Enterprise Manager additionally provides Password Loss Protection option that allows authorized Veeam users to recover data from the backup even if the encryption password is lost. If the password gets lost, the backup server will provide a challenge key for Enterprise Manager. Using asymmetric encryption with a public/private key pair, Enterprise Manager generates a response which the backup server can use for unlocking the backup file without having the password available. For more details on this feature refer to the [corresponding section ](https://helpcenter.veeam.com/docs/backup/vsphere/decrypt_without_pass.html?ver=95) of the User Guide.

The encryption algorithms used are industry standard in all cases, leveraging AES-256 and public key encryption methods. [Data Encryption](https://helpcenter.veeam.com/docs/backup/vsphere/data_encryption.html?ver=95) section of the User Guide provides detailed information on the encryption algorithms and standards used by the product.

The following sections describe encryption options available in the product, what they protect, when they should be used and best practices for their use.

## Backup and Backup Copy Job Encryption

### What does it do?

Backup and backup copy job encryption is designed to protect data at rest. These settings protect data if unauthorized user gets access to backup files outside of the backup infrastructure. Authorized users of the Veeam console do not need to know the password to restore data from encrypted backups. Encryption does not prevent authorized Veeam users from being able to access data stored in backups.

An example is the use of rotated drives for an offsite repository. Because these drives are rotated offsite, they are at a higher risk of falling into the hands of unauthorized users. Without encryption enabled, these unauthorized users could install their own copy of Veeam Backup & Replication and gain access to the stored backups easily.

On the other hand, if the backup files are encrypted, unauthorized users cannot access any data in the backups or even learn any critical information about the backup infrastructure as even backup metadata is encrypted. Without the key used for encryption or access to the original Veeam Backup & Replication console itself, the backup files remain secure.

### How does it work?

For encryption functionality to work backup encryption keys have to be generated. Those keys use mathematical symmetric cryptography and are not used to encrypt the data itself to avoid impacting backup performance. Instead, for each backup session a unique session symmetric encryption key is generated automatically and then stored in the backup file encrypted with the backup encryption key. Then each data block (compressed or not depending on the job configuration) is encrypted using the session key previously generated for the current job session and stored in the backup file. In case Password Loss Protection functionality is enabled an additional copy of session keys is stored in the backup file encrypted with the Enterprise Manager encryption keys.

This approach provides a method for encrypting backups without compromising backup performance.

### When to use it?

Backup and backup copy job encryption should be used if backups are transported offsite, or if unauthorized users may easily gain access to backup files in another way than by using the Veeam console. Common scenarios are:

-   Offsite backups to a repository using rotated drives
-   Offsite backups using unencrypted tapes
-   Offsite backups to a Veeam Cloud Connect provider
-   Regulatory or policy based requirements to store backups in encrypted form

Active full backup is required for enabling encryption to take effect if it was disabled for the job previously.

### Best Practices

-   Enable encryption if you plan to store backups in locations outside of your security domain.
-   While CPU usage for encryption is minimal for most modern processors, some amount of resources will still be consumed. If Veeam backup proxies are already highly loaded, take it into account prior to enabling job-level encryption.
-   Use strong passwords for job encryption and develop a policy for changing them regularly. Veeam Backup & Replication helps with this, as it tracks passwords’ age.
-   Store passwords in a secure location.
-   Obtain Enterprise or a higher level license for Veeam Backup & Replication, configure Veeam Backup Enterprise Manager and connect backup servers to it to enable Password Loss Protection.
-   Export a copy of the active keyset from Enterprise Manager (see [User Guide](https://helpcenter.veeam.com/docs/backup/em/em_export_import_keys.html?ver=95) for more information).
-   Back up the Veeam Backup Enterprise Manager configuration database and create an image-level backup of the Veeam Backup Enterprise Manager server. If these backups are also encrypted, make sure that passwords are not lost as there will be no Password Loss Protection for these backups.

## Tape Job Encryption

### What does it do?

Similar to backup job encryption, tape job encryption is designed to protect data at rest. These settings protect data if an unauthorized user gains access to tape media outside of the backup infrastructure. Authorized users do not need to know the password to restore data from encrypted tape backups. Encryption does not prevent authorized Veeam users from being able to access data stored in tape backups.

Typical use case is to protect data on tapes when media is shipped to an offsite location or to a 3<sup>rd</sup> party. Without encryption enabled, a lost tape could easily be accessed, and data stored on tapes could be compromised.

### How does it work?

Similar to encryption for backups on disk, a session encryption key is used to encrypt data blocks as they are written to tape. Tape encryption can leverage either hardware tape encryption (if present and enabled) or software-based encryption. If the tape drive supports hardware encryption, the session key is sent to the tape device via SCSI commands and the drive itself performs the encryption prior to writing data to tape. This allows encryption to occur with no impact on the CPU of the tape server. If the tape hardware does not support encryption, Veeam falls back automatically to using software-based AES-256 data encryption prior to sending data to the tape device.

### When to use it?

Tape job encryption should be used any time you want to protect the data stored on tape from unauthorized access by a 3<sup>rd</sup> party. Tapes are commonly transported offsite and thus have a higher chance of being lost and turning up in unexpected places. Encrypting tapes can provide an additional layer of protection if tapes are lost.

If tape jobs are writing already encrypted data to tape (for example, Veeam data from backup jobs that already have encryption enabled), you may find it acceptable to not use tape-level encryption. However, be aware that a user who gets access to the tape will be able to restore the backup files. Although this user will not be able to access the backup data in those files, some valuable information, for example, job names used for backup files, may leak.

### Best Practices

-   Enable encryption if you plan to store tapes in locations outside of your security domain.
-   Consider the risks/benefits of enabling tape job encryption even if the source data is already encrypted and evaluate appropriately the acceptable level of risk.
-   Use strong passwords for tape job encryption and develop a policy for changing them regularly (you can use Veeam Backup & Replication password age tracking capability).
-   Store passwords in a secure location.
-   Obtain Enterprise or a higher level license for Veeam Backup & Replication, configure Veeam Backup Enterprise Manager and connect backup servers to it to enable Password Loss Protection.
-   Back up the Veeam Backup Enterprise Manager configuration database and create an image-level backup of the Veeam Backup Enterprise Manager server. If these backups are also encrypted, make sure that passwords are not lost as there will be no Password Loss Protection for these backups.

## Network Transport Encryption

### What does it do?

Unlike the backup and tape job encryption features, the network transport encryption feature is designed to protect data “in-flight”. For example, when the proxy is sending data across the network to the backup repository, data can be encrypted between these two points even if job-level encryption is not enabled. This is primarily useful when the network between the source and target is not trusted, for example, when sending data across the Internet.

### How does it work?

Network encryption in Veeam Backup & Replication is controlled via the global Network Traffic options.

![Network Traffic Encryption](./encryption_1.png)

Whenever two backup infrastructure components need to communicate with each other over the IP network, a dynamic key is generated by the backup server and communicated to each node over a secure channel. The two components then establish an encrypted connection between each other using this key, and all communications between these two components for that session are then encrypted with this key. The key has a one-time use and it's discarded once the session is completed.

### When to use it?

Network transport encryption should be used if the network between two backup infrastructure components is untrusted or if the user desires to protect Veeam traffic across the network from potential network sniffing or "man in the middle" attacks.

By default, Veeam Backup & Replication automatically encrypts communication between two nodes if either one or both has an interface configured (if used or not) that is not within the RFC1918 private address space (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.0.0/16). Veeam also automatically uses network-level encryption for any connection with Veeam Cloud Connect service providers. However, Cloud Connect establishes a TLS 1.2 encrypted tunnel to the service provider in a different way. To learn more about specific Cloud Connect encryption mechanism, watch this YouTube video:  [How Veeam Cloud Connect Encryption works](https://www.youtube.com/watch?v=yGuw37PxRHU).

### Best Practices

- Enable encryption if network-level attacks are a security concern.
- Network-level encryption can use significant CPU resources, especially on the encrypting side (source) of the connection. Make sure that component nodes have enough resources. Modern CPU's can offload encryption and reduce the amount of CPU resources required. For Intel CPU's specifically, you may check your CPU model on [Intel ARK](http://ark.intel.com/search/advanced/?s=t&AESTech=true) and look for the [AES-NI](https://en.wikipedia.org/wiki/AES_instruction_set) capability.

- Use network-level encryption only where required. If backup infrastructure components are running on a network that is using non-RFC1918 IP addresses but is still private and secure from attacks, consider using the following registry key to disable automatic network-layer encryption.
  -   Path: `HKEY_LOCAL_MACHINE\SOFTWARE\Veeam\Veeam Backup and Replication`
  -   Key: `DisablePublicIPTrafficEncryption`
  -   Type: REG_DWORD
  -   Value: 1 (_default: 0_)
