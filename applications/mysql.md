# MySQL

Veeam supports backup and restore of MySQL databases.

## Backup Options:

The following options are supported to backup MySQL databases:
-	HotBackup Database Online Dump.
         o Online Dump to the same server.
         o Online Dump to Staging server
-	HotBackup Database Freeze.
-	ColdBackup Database Shutdown.

## HotBackup Database Online Dump:

There are multiple options available regarding Database Online Dump, one of the option is to use Veeam [Pre & Post Thaw Scripts]( https://helpcenter.veeam.com/docs/backup/vsphere/backup_job_vss_scripts_vm.html?ver=95) to dump the database during the backup operations and other option to dump the database to another staging server and protect the staging server from Veeam.

Let’s go through each option one by one in the details:

### Database Online Dump During Backup Operations:

In this option the pre-freeze script will dump all databases hosted on the guest to a single file under the /tmp directory. Before the VM snapshot creation, the mysql dump native command will dump a copy of the database while service will remain available.

The dump will be deleted by post-thaw script after the guest snapshot has been successful.
Pre Freeze Sciprt:

1.	Use Editor
2.	Copy the content in the editor.
```
!/bin/bash
# config:
# when running on debian we can use existing debian-sys-maint account using defaults file
# otherwise, specify username and password below using use_credentials
#use_credentials="-uroot -p"
defaults_file="/etc/my.cnf"
dump_file="/tmp/mysql_dump.sql"
database="--all-databases"
if [ -f $defaults_file ]
then
opts="--defaults-file=$defaults_file"
elif [ -n $use_credentials ]
then
opts="$opts $use_credentials"
else
echo "$0 : error, no mysql authentication method set" | logger
exit 1
fi
opts="$opts $database"
echo "$0 executing mysqldump" | logger
mysqldump $opts >$dump_file 2>/dev/null
if [ $? -ne 0 ]
then
echo "$0 : mysqldump failed" | logger
exit 2
else
echo "$0 : mysqldump suceeded" | logger
sync;sync
fi
```
3.	Save script as PreFreeze.sh
4.	Use script as [pre-freeze script]( https://helpcenter.veeam.com/docs/backup/vsphere/backup_job_vss_scripts_vm.html?ver=95)  in a backup job.

Post-Thaw Scripts
1.	 Use Editor
2.	Copy the below in the editor:
```
#!/bin/bash
dump_file="/tmp/mysql_dump.sql"
if [ -f $dump_file ]
then
echo "$0 deleting mysql dump file $dump_file" | logger
rm -f $dump_file > /dev/null 2>&1
exit 0
else
echo "$0 could not locate mysql dump file $dump
```
3.	Save file as PostThaw.sh.
4.	Use script as [Post-Thaw script]( https://helpcenter.veeam.com/docs/backup/vsphere/backup_job_vss_scripts_vm.html?ver=95)  in the backupjob

**Online Dump to Staging server

Another option is to dump the MySQL database to staging server and protect staging server from backup job.

1.	Create new server or use any existing server as NFS Share.
2.	Create Script to dump the MySQL database to Staging server
3.	Use Editor
4.	Copy below sample code in the editor:
```
#!/bin/bash
# Shell script to backup MySQL database

# Set these variables
MyUSER=""	# DB_USERNAME
MyPASS=""	# DB_PASSWORD
MyHOST=""	# DB_HOSTNAME

# Backup Dest directory
DEST="" # /home/username/backups/DB

# Email for notifications
EMAIL=""

# How many days old files must be to be removed
DAYS=3

# Linux bin paths
MYSQL="$(which mysql)"
MYSQLDUMP="$(which mysqldump)"
GZIP="$(which gzip)"

# Get date in dd-mm-yyyy format
NOW="$(date +"%d-%m-%Y_%s")"

# Create Backup sub-directories
MBD="$DEST/$NOW/mysql"
install -d $MBD

# DB skip list
SKIP="information_schema
another_one_db"

# Get all databases
DBS="$($MYSQL -h $MyHOST -u $MyUSER -p$MyPASS -Bse 'show databases')"

# Archive database dumps
for db in $DBS
do
    skipdb=-1
    if [ "$SKIP" != "" ];
    then
		for i in $SKIP
		do
			[ "$db" == "$i" ] && skipdb=1 || :
		done
    fi
 
    if [ "$skipdb" == "-1" ] ; then
    	FILE="$MBD/$db.sql"
	$MYSQLDUMP -h $MyHOST -u $MyUSER -p$MyPASS $db > $FILE
    fi
done

# Archive the directory, send mail and cleanup
cd $DEST
tar -cf $NOW.tar $NOW
$GZIP -9 $NOW.tar

echo "MySQL backup is completed! Backup name is $NOW.tar.gz" | mail -s "MySQL backup" $EMAIL
rm -rf $NOW

# Remove old files
find $DEST -mtime +$DAYS -exec rm -f {} \;
```
5.	Save file as DB_Backup.sh.
6.	Use Linux Scheduler to run the script on desired time for the backup.
7.	Configure the backup of staging VM.

***HotBackup Database Freeze.

In this option, Veeam will freeze the database during pre-freeze script and release the database in post-thaw, MySQL table will be flashed to disk into read-only state and writable once the VM snapshot has
been created.

1.	Use editor 
2.	Copy the sample code
```
#!/bin/bash
# config:
# when running on debian we can use existing debian-sys-maint account using defaults file
# otherwise, specify username and password below using use_credentials
#use_credentials="-uroot -p"
defaults_file="/etc/my.cnf"
timeout=300
lock_file=/tmp/mysql_tables_read_lock
###
if [ -f $defaults_file ]; then
opts="--defaults-file=$defaults_file"
fi
if [ -n $use_credentials ]; then
opts="$opts $use_credentials"
fi
sleep_time=$((timeout+10))
rm -f $lock_file
echo "$0 executing FLUSH TABLES WITH READ LOCK" | logger
mysql $opts -e "FLUSH TABLES WITH READ LOCK; system touch $lock_file; system nohup sleep
$sleep_time; system echo\ lock released|logger; " > /dev/null &
mysql_pid=$!
echo "$0 child pid $mysql_pid" | logger
c=0
while [ ! -f $lock_file ]
do
# check if mysql is running
if ! ps -p $mysql_pid 1>/dev/null ; then
echo "$0 mysql command has failed (bad credentials?)" | logger
exit 1
fi
sleep 1
c=$((c+1))
if [ $c -gt $timeout ]; then
echo "$0 timed out waiting for lock" | logger
touch $lock_file
kill $mysql_pid
fi
done
echo $mysql_pid > $lock_file
exit 0
```
3.	Save as PreFreeze.sh.
4.	Configure the script as prefreeze script in the backup job.

Post-Thaw Script:
1.	Use Editor
2.	Copy the sample code
```
#!/bin/bash
lock_file=/tmp/mysql_tables_read_lock
###
mysql_pid=$(cat $lock_file)
echo "$0 sending sigterm to $mysql_pid" | logger
pkill -9 -P $mysql_pid
rm -f $lock_file
exit 0
```
3.	Save code as Post-Thaw.sh 
4.	Configure post-thaw script in the backup job.

*Tip* 
> Adjust the timeout according to database size, in the sample script we have set 300 seconds for timeout

## Cold Backup Database Shutdown:

In this option, Veeam will use pre and post-thaw script to stop and start the MySQL service using init.d or systemctl commands, depending on the database packages during the snapshot operations.

#### Pre-Freeze Script

1.	Use Editor
2.	Copy the sample code below
```
#!/bin/bash
timeout=300
if [ -f /var/run/mysqld/mysqld.pid ]
then
mysql_pid=$(cat /var/run/mysqld/mysqld.pid) >/dev/null 2>&1
else
echo "$0 : Mysql not started or bad mysql pid file location" | logger
exit 1
fi
echo "$0 : Processing pre-freeze backup script" | logger
/etc/init.d/mysqld stop mysql & > /dev/null 2>&1
c=0
while [ true ]
do
if [ $c -gt $timeout ]
then
echo "$0 : timed out, mysql shutdown failed" | logger
exit 2
fi

# check if mysql is running
if [ -f /var/run/mysqld/mysqld.pid ]
then
echo "$0 : Waiting 5 more seconds for mysql shutdown" | logger
sleep 5
c=$((c+5))
else
echo "$0 : Mysql stopped" | logger
sync;sync
break

fi
done
```
3.	Save code as Pre-Freeze.sh
4.	Configure the script to run with backup job as pre-freeze script.

#### Post-Thaw Script:

1.	Use Editor
2.	Copy the sample code below
```
#!/bin/bash
timeout=300
echo "$0 : processing post-thaw backup script" | logger
if [ -f /var/run/mysqld/mysqld.pid ]
then
mysql_pid=$(cat /var/run/mysqld/mysqld.pid) >/dev/null 2>&1
echo "$0 : Mysql already started with PID $mysql_pid" | logger
exit 1
fi
/etc/init.d/mysqld start mysql & > /dev/null 2>&1
c=0
while [ true ]
do
if [ $c -gt $timeout ]
then
echo "$0 : timed out, mysql startup failed" | logger
exit 2
fi
# check if mysql is running
if [ -f /var/run/mysqld/mysqld.pid ]
then
mysql_pid=$(cat /var/run/mysqld/mysqld.pid) >/dev/null 2>&1
echo "$0 : MySQL started with pid $mysql_pid" | logger
break
else
echo "$0 : Waiting 5 more seconds for mysql startup"
sleep 5
c=$((c+5))
fi
done
```
3.	Save code as Postthaw.sh 
4.	Configure the backup job to run the script as Post Thaw Script.

# Restore:
The restore is the integrated part of MySQL protection strategy.
Veeam provides multiple option of MySQL restores depends on the backup method.
Let’s go through the option for each backup method.

### Database Online Dump During Backup Operations:
For this backup option, Veeam provides following restore options depends on the failure:

| Failure   | Restore Option |
| ------------- | ------------- |
| Server Failed | Instant Server Restore  |
| Database or Application Level Failure | Guest File Level Restore  |
| Database Item Level Restore             | Veeam Universal Application Item Restore         


### Online Dump to Staging server
In this backup job, Veeam provides following restore options 

| Failure   | Restore Option |
| ------------- | ------------- |
| Database Restore             | Instant File Level Restore |        

*Tip*
> In addition to online dump to staging server, take crash-consistency backup of mysql server and in case of server failure restore the mysql server from crach-consistency backup and use database dump from staging server to restore the database.

### HotBackup Database Freeze.
For this backup option, Veeam provides following restore options depends on the failure:

| Failure   | Restore Option |
| ------------- | ------------- |
| Server Failed | Instant Server Restore  |
| Database or Application Level Failure | Guest File Level Restore  |
| Database Item Level Restore             | Veeam Universal Application Item Restore         

### ColdBackup Database Shutdown.
For this backup option, Veeam provides following restore options depends on the failure:

| Failure   | Restore Option |
| ------------- | ------------- |
| Server Failed | Instant Server Restore  |
| Database or Application Level Failure | Guest File Level Restore  |
| Database Item Level Restore             | Veeam Universal Application Item Restore         

For more details about protection and restore use [MySQL Protection Whitepaper]( https://login.veeam.com/auth/realms/veeamsso/protocol/openid-connect/auth/?scope=profilehttps://www.veeam.com/consistent-protection-mysql-mariadb_wpp.pdfresponse_type=codehttps://www.veeam.com/consistent-protection-mysql-mariadb_wpp.pdfredirect_uri=https%3A%2F%2Fwww.veeam.com%2Fservices%2Fauthentication%2Fredirect_urlhttps://www.veeam.com/consistent-protection-mysql-mariadb_wpp.pdfstate=eyJmaW5hbFJlZGlyZWN0TG9jYXRpb24iOiJodHRwczovL3d3dy52ZWVhbS5jb20vY29uc2lzdGVudC1wcm90ZWN0aW9uLW15c3FsLW1hcmlhZGJfd3BwLnBkZiJ9https://www.veeam.com/consistent-protection-mysql-mariadb_wpp.pdfclient_id=aemhttps://www.veeam.com/consistent-protection-mysql-mariadb_wpp.pdfrestarted=true)  
