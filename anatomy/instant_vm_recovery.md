# Instant VM Recovery

## Step by step description of the IVMR process implemented in Veeam Backup and Replication

![](.\vPowerNFS_1.png)

### 1. Initialization Phase

In the initialization phase, Veeam Backup & Replication prepares
resources necessary for Instant VM Recovery. It performs the following
steps:

- Starts the Veeam Backup Manager process on the Veeam backup server.
- Checks with the Veeam Backup Service whether the necessary backup infrastructure resources are available for instant VM Recovery.
- Communicates with the Transport Service on the backup repository to
    start Veeam Data Mover.

### 2. NFS Mapping

When backup infrastructure resources are prepared, Veeam Backup &
Replication maps an empty NFS datastore to the selected ESXi host. It
uses the Veeam vPower NFS Service for this purpose.

Next, Veeam Backup & Replication creates in the Veeam NFS datastore VM
configuration files and links to virtual disk files. Virtual disk files
remain in the backup on the repository, while all changes to these files
are written to the cache file.

### 3. Registering and Starting VM

The VM runs from the Veeam NFS datastore. VMware vSphere treats the
Veeam NFS datastore as any regular datastore. For this reason, with the
recovered VM you can perform all actions that vCenter Server/ESXi
supports for regular VMs.

### 4. Migrating guest to production datastore
To migrate VM disk data to a production datastore, use VMware Storage
vMotion or Veeam Quick Migration. For details, see [Veeam Backup &
Replication User
Guide](https://helpcenter.veeam.com/docs/backup/vsphere/migration_job.html?ver=95).

## Performance concerns

### Read pattern

Usually reseved for the guests requiring the best possible RTOs, the IVMR process is read intensive and its performance is directly related to the performance of the underlying repository. Very good results can obtained from standard drives repositories (sometimes even offering faster boot time than the production guest) while deduplication appliances might be considered carefully for such kind of use.

Keep in mind that when working on its backup files to start the guest, Veeam Backup and Replication needs to access the metadatas, which is generating some random small blocks read pattern on the repository.

### Write redirections

Once booted, the guest will read existing blocks from the backup storage and write/re-read new blocks on the configured storage (whether beeing a datastore or a temporary file on the vPower NFS server local drive  in the folder "%ALLUSERSPROFILE%\Veeam\Backup\NfsDatastore"). To ensure consistent performances during the IVMR process, it is recommended to redirect the writes of the restored guest on a production datastore.