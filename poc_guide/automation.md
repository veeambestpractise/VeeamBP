# Automation
The bigger the environment, the more automation is needed to reduce the administration effort. For example, if you are operating 40 branch offices with independent Veeam installations, you may want to roll out and configure backup servers with scripts, and automatically create jobs in the same location. Another example is automatic job creation for 2,000-3,000 VMs with exactly the same configurations, which can limit user-caused misconfiguration.

## Command line
Following operations are managed through the Windows command line:

* Installation - [Link to Help Center](https://helpcenter.veeam.com/docs/backup/vsphere/silent_mode.html?ver=95)
* Updates - [Link to Help Center](https://helpcenter.veeam.com/docs/backup/vsphere/update_unattended.html?ver=95)

## PowerShell
Operations in Veeam Backup & Replication can be automated with Veeam PowerShell snap-in in the following areas:

* Configuration
* Job creation/job editing
* Working with external schedulers (UC4/TWS and other) to start Veeam jobs
* Restores
* Reporting
* Datacenter migration (quick migration or replication)

The PowerShell plugin is available with all commercial versions of the product.

**Note:**	PowerShell plugin is also available with Veeam Backup FREE, although limited: https://www.veeam.com/blog/veeam-backup-free-edition-now-with-powershell.html

Our customers and partners use this functionality to scale out backup infrastructure environments to nearly 100,000 VMs under a single Veeam Backup Enterprise Manager instance with multiple backup servers located in different datacenters.

The best starting point to get in touch with the Veeam PowerShell plugin is to read the Veeam PowerShell User Guide > [Veeam Help Center - PowerShell Reference](https://helpcenter.veeam.com/docs/backup/powershell/getting_started.html?ver=95).

You can find help for the scripts in the [Veeam Community Forums - PowerShell](http://forums.veeam.com/powershell-f26/) section. If you need some examples, refer to the following thread: [Getting Started and Code Examples](https://forums.veeam.com/powershell-f26/getting-started-and-code-examples-t13372.html)

## RESTful API
In the Veeam Enterprise Manager, there is as well RESTful API that allows you to create workflows in orchestration tools or to integrate Veeam Backup Enterprise Manager (self-services) in your own “cloud” portal. Specifically, this is an option that comes with Enterprise Plus Editions and is focused on the hosting business.

Here is a list of external resources:
* [Veeam Help Center - RESTful API Reference ](https://helpcenter.veeam.com/docs/backup/rest/overview.html?ver=95)
* [Veeam Community Forums](https://forums.veeam.com/restful-api-f30/)
* [Veeam Help Center - Beginner Example](https://helpcenter.veeam.com/docs/backup/rest/beginner_example.html?ver=95)

## A simple RESTful API example - adding a guest to a backup job

In the following section, the Veeam WEB client will be used for convenience as it is quite simple by nature and instantly available through enterprise manager URL.  Also, the browser used is configured to accept cookies to simplify the authentication token management.

### Authentication on the REST server

From the client browser, connect to the URL http://EM:9399/web/#/api/ and enter credentials as requested. Then, follow the latest version URL to get the list of all accessible resources types. http://EM:9399/web/#/api/sessionMngr/?v=latest

###	Building a query to retrieve the vCenter UID

Once logged in, knowing the vCenter Name where the VM we want to add resides, we need to get the vCenter UID.

Refering to the REST API guide https://helpcenter.veeam.com/docs/backup/rest/get_managedservers_id.html?ver=95 we can gather necessary informations to build a query.
* Object type is “ManagedServer”
* Property to filter is “ManagedServerType” from which “VC” corresponds to vCenter
* Property to filter is “Name” equal to “vc.democenter.int” in this example

**Note:** the “ManagedServerType” has been added to the query for demonstration purpose.

http://EM:9399/web/#/api/query?type=ManagedServer&filter=(ManagedServerType==VC;Name==”vcsa.democenter.int

    <?xml version="1.0" encoding="UTF-8"?>
    <QueryResult xmlns="http://www.veeam.com/ent/v1.0" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <Refs>
        <Ref UID="urn:veeam:ManagedServer:93fe5565-0ae7-4574-abb5-0f4ea8c5e9bd" Name="vcsa.democenter.int" Href="http://hq-vbrem1.democenter.int:9399/api/managedServers/93fe5565-0ae7-4574-abb5-0f4ea8c5e9bd" Type="ManagedServerReference">
          <Links>
            <Link Href="http://hq-vbrem1.democenter.int:9399/api/managedServers/93fe5565-0ae7-4574-abb5-0f4ea8c5e9bd?format=Entity" Name="vcsa.democenter.int" Type="ManagedServer" Rel="Alternate"/>
            <Link Href="http://hq-vbrem1.democenter.int:9399/api/backupServers/d7b8bcdd-dbc5-40a3-9a50-dd8ba65cfa91" Name="hq-vbr1.democenter.int" Type="BackupServerReference" Rel="Up"/>
          </Links>
        </Ref>
      </Refs>
      <PagingInfo PageNum="1" PageSize="100" PagesCount="1">
        <Links>
          <Link Href="http://hq-vbrem1.democenter.int:9399/api/query?type=ManagedServer&filter=(ManagedServerType%3d%3dVC%3bName%3d%3d%22vcsa.democenter.int%22)&pageSize=100&page=1" Rel="First"/>
          <Link Href="http://hq-vbrem1.democenter.int:9399/api/query?type=ManagedServer&filter=(ManagedServerType%3d%3dVC%3bName%3d%3d%22vcsa.democenter.int%22)&pageSize=100&page=1" Rel="Last"/>
        </Links>
      </PagingInfo>
    </QueryResult>

The lookup service necessitates a “HierarchyRoot” resource type in the urn, which is an alternate representation of the “ManagedServer”. We then must send a GET to the managed server resource representation: http://EM:9399/web/#/api/managedServers/25fb843d-92a3-45d4-836c-0531afe4df9b?format=Entity and find the “Alternate” representation of type “HierarchyRoot” in the proposed links.

    <Link Href="http://hq-vbrem1.democenter.int:9399/api/hierarchyRoots/93fe5565-0ae7-4574-abb5-0f4ea8c5e9bd" Name="vcsa.democenter.int" Type="HierarchyRootReference" Rel="Alternate"/>

From here, send a GET request to the HierarchyRoot resource representation to pick up its UID (simply clicking on the URL will send the GET request).

http://hq-vbrem1.democenter.int:9399/api/hierarchyRoots/93fe5565-0ae7-4574-abb5-0f4ea8c5e9bd?format=Entity

    <?xml version="1.0" encoding="UTF-8"?>
    <HierarchyRoot Href="http://hq-vbrem1.democenter.int:9399/api/hierarchyRoots/93fe5565-0ae7-4574-abb5-0f4ea8c5e9bd?format=Entity" Type="HierarchyRoot" Name="vcsa.democenter.int" UID="urn:veeam:HierarchyRoot:93fe5565-0ae7-4574-abb5-0f4ea8c5e9bd" xmlns="http://www.veeam.com/ent/v1.0" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <Links>
        <Link Href="http://hq-vbrem1.democenter.int:9399/api/backupServers/d7b8bcdd-dbc5-40a3-9a50-dd8ba65cfa91" Name="hq-vbr1.democenter.int" Type="BackupServerReference" Rel="Up"/>
        <Link Href="http://hq-vbrem1.democenter.int:9399/api/hierarchyRoots/93fe5565-0ae7-4574-abb5-0f4ea8c5e9bd" Name="vcsa.democenter.int" Type="HierarchyRootReference" Rel="Alternate"/>
        <Link Href="http://hq-vbrem1.democenter.int:9399/api/managedServers/93fe5565-0ae7-4574-abb5-0f4ea8c5e9bd?format=Entity" Name="vcsa.democenter.int" Type="ManagedServer" Rel="Related"/>
      </Links>
      <HierarchyRootId>93fe5565-0ae7-4574-abb5-0f4ea8c5e9bd</HierarchyRootId>
      <UniqueId>FFB4D8B6-CEC0-4DF8-87D5-82D931ED6FBD</UniqueId>
      <HostType>VC</HostType>
    </HierarchyRoot>

The required reference for further use is the UID “urn:veeam:HierarchyRoot:93fe5565-0ae7-4574-abb5-0f4ea8c5e9bd” corresponding to the Veeam managed vCenter server where the VM should reside.

**Note:** It could have been more simple to directly work on the ManagedServer UID and directly change the resource type from “ManagedServer” to “HierarchyRoot”. The complex method was chosen for demonstration purpose.

###	Building a lookup to retrieve the virtual machine ID

Knowing the UID of the “Host” (vCenter), and the name of the guest we want to add to a job, we can build the lookup URL using the name of the VM as a selection criteria. The rules to build the lookup request are detailed in the REST API guide : https://helpcenter.veeam.com/docs/backup/rest/lookup_query.html?ver=95#params.

http://hq-vbrem1.democenter.int:9399/web/#/api/lookup?host=urn:veeam:HierarchyRoot:93fe5565-0ae7-4574-abb5-0f4ea8c5e9bd&name=demo-win1&type=Vm

    <?xml version="1.0" encoding="UTF-8"?>
    <HierarchyItems xmlns="http://www.veeam.com/ent/v1.0" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <HierarchyItem Type="HierarchyItem">
        <ObjectRef>urn:VMware:Vm:93fe5565-0ae7-4574-abb5-0f4ea8c5e9bd.vm-48911</ObjectRef>
        <ObjectType>Vm</ObjectType>
        <ObjectName>demo-win1</ObjectName>
      </HierarchyItem>
    </HierarchyItems>

The UID here is given by the “ObjectRef” property: “urn:VMware:Vm:93fe5565-0ae7-4574-abb5-0f4ea8c5e9bd.vm-48911”. As you can see, the UID of the VM comprises the UID of the management server appended with the Mo-Ref of the VM. This is useful if you want to automatically build a Veeam VM reference, knowing its management server and Mo-Ref. This “manual” type construction of references can be used for automation purpose.

### Building a query to retrieve the Job ID

Knowing the Name of the job where the VM should be added (“Test REST”) we can request the query service to get its ID:

http://hq-vbrem1.democenter.int:9399/web/#/api/query?type=job&filter=(Name==%22Test%20REST%22)

    <?xml version="1.0" encoding="UTF-8"?>
    <QueryResult xmlns="http://www.veeam.com/ent/v1.0" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <Refs>
        <Ref UID="urn:veeam:Job:455c0799-ede5-4ade-a7b2-02d2d0fac3de" Name="Test REST" Href="http://hq-vbrem1.democenter.int:9399/api/jobs/455c0799-ede5-4ade-a7b2-02d2d0fac3de" Type="JobReference">
          <Links>
            <Link Href="http://hq-vbrem1.democenter.int:9399/api/backupServers/d7b8bcdd-dbc5-40a3-9a50-dd8ba65cfa91" Name="hq-vbr1.democenter.int" Type="BackupServerReference" Rel="Up"/>
            <Link Href="http://hq-vbrem1.democenter.int:9399/api/jobs/455c0799-ede5-4ade-a7b2-02d2d0fac3de?format=Entity" Name="Test REST" Type="Job" Rel="Alternate"/>
            <Link Href="http://hq-vbrem1.democenter.int:9399/api/jobs/455c0799-ede5-4ade-a7b2-02d2d0fac3de/backupSessions" Type="BackupJobSessionReferenceList" Rel="Down"/>
          </Links>
        </Ref>
      </Refs>
      <PagingInfo PageNum="1" PageSize="100" PagesCount="1">
        <Links>
          <Link Href="http://hq-vbrem1.democenter.int:9399/api/query?type=job&filter=(Name%3d%3d%22Test+REST%22)&pageSize=100&page=1" Rel="First"/>
          <Link Href="http://hq-vbrem1.democenter.int:9399/api/query?type=job&filter=(Name%3d%3d%22Test+REST%22)&pageSize=100&page=1" Rel="Last"/>
        </Links>
      </PagingInfo>
    </QueryResult>

The ID is given by the last part of the Ref UID : “urn:veeam:Job:455c0799-ede5-4ade-a7b2-02d2d0fac3de”.
The URL to access the job resource representation is directly given by the link pointing to the “JobReference” type: http://hq-vbrem1.democenter.int:9399/api/jobs/455c0799-ede5-4ade-a7b2-02d2d0fac3de

**Note:** To access the resource (not the resource representation) and get more details, you shall follow the “Alternate” related object, which type is “Job” and not “JobReference”.

### Adding the VM to the job

Knowing the “Jobs” resource representation structure, the resource to be called to add the VM to the job is "/jobs/{ID}/includes" with a POST verb. In case of any doubt about the resource to call, the REST reference guide offers a precise representation of the resource tree: https://helpcenter.veeam.com/docs/backup/rest/post_jobs_id_includes.html?ver=95

As stated by the “Min/Max” column, the only mandatory parameters to add in the request body are the container reference (a VM in our example) and name “HierarchyObjRef” and “HierarchyObjName”.

All other guest related parameters are described in the documentation. Specific credentials for inguest processing are described by the resource “/backupServers/{ID}/credentials”.
- Order 
- GuestProcessingOptions
	- VssSnapshotOptions
	- WindowsGuestFSIndexingOptions
	- LinuxGuestFSIndexingOptions
	- SQLBackupOptions
	- WindowsCredentialsId
	- LinuxCredentialsId
	- FSFileExcludeOptions
	- OracleBackupOptions

We will then form a HTTP phrase: 
Type: POST

**URL:** http://hq-vbrem1.democenter.int:9399/web/#/api/jobs/455c0799-ede5-4ade-a7b2-02d2d0fac3de/includes

**Header:** (automatically handled by the client since cookies are in use) :

**Cookie:** X-RestSvcSessionId=Session_ID

**Body:**

    <?xml version="1.0" encoding="UTF-8"?>
	<CreateObjectInJobSpec xmlns="http://www.veeam.com/ent/v1.0" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <HierarchyObjRef>urn:VMware:Vm:93fe5565-0ae7-4574-abb5-0f4ea8c5e9bd.vm-48911</HierarchyObjRef>
        <HierarchyObjName>demo-win1</HierarchyObjName>
    </CreateObjectInJobSpec>

To access the POST request from the Veeam WEB client, open the resource view of the job ID 455c0799-ede5-4ade-a7b2-02d2d0fac3de and follow the proposed link leading to add a VM in the job (Type=”ObjectInJob”, Rel=”Create”).

    <Link Href="http://hq-vbrem1.democenter.int:9399/api/jobs/455c0799-ede5-4ade-a7b2-02d2d0fac3de/includes" Type="ObjectInJob" Rel="Create"/>

This will automatically form the HTTP request :
 
From there, the body can be modified to indicate proper VM reference:

    <?xml version="1.0" encoding="utf-8"?>
    <CreateObjectInJobSpec xmlns="http://www.veeam.com/ent/v1.0" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <HierarchyObjRef>urn:VMware:Vm:93fe5565-0ae7-4574-abb5-0f4ea8c5e9bd.vm-48911</HierarchyObjRef>
        <HierarchyObjName>demo-win1</HierarchyObjName>
    </CreateObjectInJobSpec>

Upon completion, a return code 200 should be sent by the server, pointing to the corresponding task.

To verify if the added VM is in the job, we can send a quuery using the “ObjectInJob” type as described in the available querying type (refer to user guide “Query Syntax” section for more informations). The possible filter parameters are described in the “(GET) /jobs/{ID}/includes/{ID}” section of the reference guide.

http://hq-vbrem1.democenter.int:9399/web/#/api/query?type=ObjectInJob&filter=(JobName==”Test REST”;Name==”demo-win1”)

    <?xml version="1.0" encoding="UTF-8"?>
    <QueryResult xmlns="http://www.veeam.com/ent/v1.0" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <Resources>
        <sInObjectJob>
          <ObjectInJob Href="http://hq-vbrem1.democenter.int:9399/api/jobs/455c0799-ede5-4ade-a7b2-02d2d0fac3de/includes/8242bd6d-1aaf-41d7-9a11-e51fad56318f" Type="ObjectInJob">
            <Links>
              <Link Href="http://hq-vbrem1.democenter.int:9399/api/jobs/455c0799-ede5-4ade-a7b2-02d2d0fac3de/includes/8242bd6d-1aaf-41d7-9a11-e51fad56318f" Rel="Delete"/>
              <Link Href="http://hq-vbrem1.democenter.int:9399/api/jobs/455c0799-ede5-4ade-a7b2-02d2d0fac3de?format=Entity" Name="Test REST" Type="Job" Rel="Up"/>
            </Links>
            <ObjectInJobId>8242bd6d-1aaf-41d7-9a11-e51fad56318f</ObjectInJobId>
            <HierarchyObjRef>urn:VMware:Vm:93fe5565-0ae7-4574-abb5-0f4ea8c5e9bd.vm-48911</HierarchyObjRef>
            <Name>demo-win1</Name>
            <DisplayName>demo-win1</DisplayName>
            <Order>1</Order>
            <GuestProcessingOptions>
              <VssSnapshotOptions>
                <VssSnapshotMode>Disabled</VssSnapshotMode>
                <IsCopyOnly>false</IsCopyOnly>
              </VssSnapshotOptions>
              <WindowsGuestFSIndexingOptions>
                <FileSystemIndexingMode>Disabled</FileSystemIndexingMode>
                <IncludedIndexingFolders/>
                <ExcludedIndexingFolders/>
              </WindowsGuestFSIndexingOptions>
              <LinuxGuestFSIndexingOptions>
                <FileSystemIndexingMode>Disabled</FileSystemIndexingMode>
                <IncludedIndexingFolders/>
                <ExcludedIndexingFolders/>
              </LinuxGuestFSIndexingOptions>
              <SqlBackupOptions>
                <TransactionLogsProcessing>OnlyOnSuccessJob</TransactionLogsProcessing>
                <BackupLogsFrequencyMin>15</BackupLogsFrequencyMin>
                <UseDbBackupRetention>true</UseDbBackupRetention>
                <RetainDays>15</RetainDays>
              </SqlBackupOptions>
		      <WindowsCredentialsId>00000000-0000-0000-0000-000000000000</WindowsCredentialsId>
              <LinuxCredentialsId>00000000-0000-0000-0000-000000000000</LinuxCredentialsId>
            </GuestProcessingOptions>
          </ObjectInJob>
        </sInObjectJob>
      </Resources>
      <PagingInfo PageNum="1" PageSize="100" PagesCount="1">
        <Links>
          <Link Href="http://hq-vbrem1.democenter.int:9399/api/query?type=ObjectInJob&filter=(JobName%3d%3d%22Test+REST%22%3bName%3d%3d%22demo-win1%22)&pageSize=100&page=1" Rel="First"/>
          <Link Href="http://hq-vbrem1.democenter.int:9399/api/query?type=ObjectInJob&filter=(JobName%3d%3d%22Test+REST%22%3bName%3d%3d%22demo-win1%22)&pageSize=100&page=1" Rel="Last"/>
        </Links>
      </PagingInfo>
    </QueryResult>

### Closing the connection
The final step is to close the connection. Using the VEEAM REST client, closing the client will close the connection. Using any other client, a DELETE should be sent to the session resource representation (leaving the body empty, as the session is referenced to in the URL as a resource).