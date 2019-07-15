# IBM Lotus Domino
Veeam supports the backup and restores of IBM Lotus Domino.
## Background
To protect the Lotus Domino following files and folder are required to be backup:
-	Domino server data files
-	All databases
-	Template files
-	notes.ini file
-	ID files
-	Mail.box
As IBM Lotus Domino is a non VSS-aware application, to take the consistent backup of Lotus Domino, we will use the methods explained in the next section.

## Procedure: 
In this section, we will create the scripts to be run to take a consistent backup of Lotus Domino.
There are two methods to take backup of IBM Lotus Domino:
-	Domino Online Backup.
-	Domino Service Shutdown & Start.
### Domino Online Backup:
This will close all the connection and write the RAM to the disk, but beware that client can reopen a database at any point in time, snapshot on average take 3-5 seconds select a time which is off-production when very fewer clients are connected.
To use this ontion, follow the steps below:
1.	Open a notepad
2.	Copy the content in the notepad.
‘’’’
c:\Domino\nserver.exe -c "drop all"
timeout /t 10 /nobreak
c:\domino\nserver.exe -c "dbcache flush"
timeout /t 30 /nobreak
‘’’’
3.	Save the file as “OnlineBackup.bat”

Copy the script to Veeam Backup Server, and configure the job to run it as pre-freeze . Please click on the link for more information about [VSS Scripts](https://helpcenter.veeam.com/docs/backup/vsphere/backup_job_vss_scripts_vm.html?ver=95) 


### Domino Service Shutdown & Start:
In this method we will use commands to stop domaino service as pre-freeze script and post-thaw script will start the domino services, it will have around 5-15 seconds downtime depends on the server performance.
This method will ensure 100% consistency backup.

To use this option, follow the step below:
Pre-Backup Script:
1.	Open a notepad.
2.	Copy the contents:
     ‘’’
net stop “Lotus Domino Server (DominoData)”
‘’’
3.	Save the file as “PreFreezeScript.bat”
Post-Thaw Script:
1.	Open a notepad.
2.	Copy the contents:
‘’’
net start "Lotus Domino Server (DominoData)"
‘’’
3.	Save the file as “post-thaw.bat”

Copy the scripts to Veeam Backup Server, and configure the job to run pre-freeze and post-thaw scripts. Please click on the link for more information about [VSS Scripts](https://helpcenter.veeam.com/docs/backup/vsphere/backup_job_vss_scripts_vm.html?ver=95) 

## Restores:
Restores is the integrated part of IBM Lotus Domaino protection, Veeam offers followings option to restore IBM Lotus Domino Server:
1.	Instant Server Restore – Instant VM Recovery.
2.	Instant Individual Emails Restore. 	

###Instant Server Restore – Instant VM Recovery:
In case of complete server failure, you can use Veeam Instant VM Restore to bring back the Domino server in less than 15 mints*
### Instant Individual Emails Restore:
In order to recover the individual emails, please follow the steps below:
1.	Install a Note Client. (User should have full access to production database)
2.	Start Instant File Level Restore.
3.	Access NSF files under the c:\VeeamFLR path and subfolders (All Domino Server Disks are mounted on this path).
4.	Select the emails and copy back to production mailbox.
5.	If DAOS enabled on the Domino Server, You can search the missing file and restore with Veeam Instant File Level Restore.  For more information please check [Lotus KB](https://www-10.lotus.com/ldd/dominowiki.nsf/dx/Archiving_and_recovering_IBM_Lotus_DAOS-enabled_databases) 


*Note:*
>Currently, there is no option to work with Domino Log files, you may consider changing transaction logging to circular logging follow >the [Lotus KB](https://www.ibm.com/support/knowledgecenter/en/SSKTMJ_9.0.1/admin/admn_settingupadominoserverfortransactionlogging_t.html) to change the transaction logging option  
