Welcome to Veeam Backup & Replication Best Practise V9.5u4a
===========================================
.. |date| date::

Last Updated on |date|


Veeam Best Practice V9.5u4a
======================

.. toctree::
   :caption: Welcome
   :titlesonly:
   :maxdepth: 3

    About Veeam Backup & Replication Best Practices <README>
    Introduction <introduction/readme>
	Contacting Veeam Software <introduction/contacting_veeam_software>
    DNS Resolution <resource_planning/dns_resolution>

.. toctree::
   :caption: Veeam Backup Server
   :titlesonly:
   :maxdepth: 3

	Veeam Backup Server <resource_planning/backup_server_introduction>
    Deployment Method <resource_planning/backup_server_deployment_method>
    Backup Server Placement <resource_planning/backup_server_placement>
    Sizing and System Requirements <resource_planning/backup_server_sizing>
    Veeam Backup & Replication Database <resource_planning/backup_server_database>
    Protecting Veeam Backup & Replication Configuration <resource_planning/protecting_veeam_backup_and_replication_config>

.. toctree::
   :caption: Veeam Enterprise Manager
   :titlesonly:
   :maxdepth: 3

	Veeam Enterprise Manager <resource_planning/veeam_enterprise_manager>
    vCloud Director Self Service Portal <resource_planning/veeam_vcloud_director_portal>

.. toctree::
   :caption: Search Servers
   :titlesonly:
   :maxdepth: 3

	Search Server and Indexing <resource_planning/search_server_and_indexing>

.. toctree::
   :caption: Veeam Proxy Services
   :titlesonly:
   :maxdepth: 3

	Proxy Servers - Introduction <resource_planning/proxy_servers_intro>
    Proxy - VMware vSphere <resource_planning/proxy_server_vmware-vsphere>
    Transport Modes <resource_planning/transport_modes>
    Direct Storage Access <resource_planning/direct_san>
    Virtual Appliance Mode <resource_planning/virtual_appliance_mode>
    Network Mode <resource_planning/network_mode>
    Backup from Storage Snapshots <resource_planning/backup_from_storage_snapshots>
    NetApp Data ONTAP integration <resource_planning/backup_from_storage_snapshots_netapp>
    Nimble Storage integration <resource_planning/backup_from_storage_snapshots_nimble>
    Selecting a Transport Mode <resource_planning/selecting_a_transport_mode>
    Sizing a Backup Proxy <resource_planning/sizing_a_backup_proxy>
    Proxy - Microsoft Hyper-V <resource_planning/proxy_server_ms-hyperv>
    Proxy - Nutanix AHV <resource_planning/proxy_server_nutanix-ahv>

.. toctree::
   :caption: Primary and Secondary Storage BP
   :titlesonly:
   :maxdepth: 3

	  HPE 3PAR VMs disks considerations <storage_bps/3par_vs_thin-disks>
    DellEMC Data Domain advanced scalability <storage_bps/datadomain_adv-scalability>

.. toctree::
   :caption: Veeam Repository Services
   :titlesonly:
   :maxdepth: 3

	Backup Repository <resource_planning/repository_server>
    Repository Types <resource_planning/repository_types>
    SMB <resource_planning/repository_type_smb>
    Deduplication Appliances <resource_planning/repository_type_dedupe>
    Integration specifics <resource_planning/repository_type_dedupe_integrated>
    Windows Server Deduplication <resource_planning/repository_type_dedupe_windows>
    Object Storage <resource_planning/repository_type_object>
    Repository Planning <resource_planning/repository_planning>
    Sizing <resource_planning/repository_planning_sizing>
    Per VM Backup Files <resource_planning/repository_planning_pervm>
    Scale-out Backup Repository <resource_planning/repository_sobr>
    Capacity Tier <resource_planning/repository_sobr_capacity_tier>

.. toctree::
   :caption: Wan Acceleration
   :titlesonly:
   :maxdepth: 3


	WAN Acceleration <resource_planning/wan_acceleration>
    Analyzing Wan Acceleration Workload <resource_planning/Analysing_Wan_Acceleration_Workload>
    Comparing WAN Acceleration Modes <resource_planning/Comparing_Wan_Acceleration_Modes>
    Sizing For WAN Acceleration <resource_planning/Sizing_for_Wan_Acceleration>
    Sizing Targets for WAN Accereration  Relationship <resource_planning/Sizing_Targets_for_relationships>
    Deployments For WAN Acceleration <resource_planning/Deployments_for_Wan_Acceleration>
    Is WAN Acceleration Right For me <resource_planning/Is_Wan_Acceleration_right_for_my_environment>

.. toctree::
   :caption: Tape Support
   :titlesonly:
   :maxdepth: 3

	Tape Support <resource_planning/tape_support-intro>
    Tape Deployments <resource_planning/tape_support-deploy>
    Tape Media Information <resource_planning/tape_support-media>
    Tape Config Requirements <resource_planning/tape_support-config>
    Tape Parallel Processing <resource_planning/tape_support-pp>
    Tape Virtual Full <resource_planning/tape_support-VF>
    Tape Writing to Tape <resource_planning/tape_support-totape>
    Tape Restores <resource_planning/tape_support-restore>

.. toctree::
   :caption: Veeam Explorers
   :titlesonly:
   :maxdepth: 3

	Veeam Explorers <resource_planning/veeam_explorers>

.. toctree::
   :caption: vSphere
   :titlesonly:
   :maxdepth: 3

	Interaction with VMware vSphere <resource_planning/interaction_with_vsphere>

.. toctree::
   :caption: Hyper-V
   :titlesonly:
   :maxdepth: 3

	Interaction with Microsoft Hyper-V <Hyper-V/Hyper-V>

.. toctree::
   :caption: Job Configuration Considerations
   :titlesonly:
   :maxdepth: 3

	Job Configuration <job_configuration/README>
    Backup Methods <job_configuration/backup_methods>
    Encryption <job_configuration/encryption>
    Deduplication and Compression <job_configuration/deduplication_and_compression>
    Backup Job <job_configuration/backup_job>
    Backup Copy Job <job_configuration/backup_copy_job>
    Replication Job <job_configuration/replication_job>
    Application-Aware Image Processing <job_configuration/application_aware_image_processing>

.. toctree::
   :caption: Data Verification Services
   :titlesonly:
   :maxdepth: 3

	Data Verification Using Virtual Labs <resource_planning/vpower_nfs_and_virtual_lab>

.. toctree::
   :caption: Application Support
   :titlesonly:
   :maxdepth: 3

	Overview of Applications Support <applications/README>
    Active Directory <applications/active_directory>
    Microsoft Exchange <applications/exchange>
    Microsoft SQL Server <applications/sql_server>
    Microsoft SharePoint Server <applications/sharepoint>
    Oracle Database <applications/oracle>
    MySQL <applications/mysql>
    IBM Notes/Domino <applications/domino>
    SAP HANA <applications/sap_hana>

.. toctree::
   :caption: Guides and Assesments
   :titlesonly:
   :maxdepth: 3

	POC Guide <poc_guide/README>
    Assessment <poc_guide/assessment>
    Accelerated Evaluation <poc_guide/accelerated_evaluation>
    Enhanced Evaluation <poc_guide/enhanced_evaluation>
    Workshop Example <poc_guide/enhanced_evaluation_example>
    Preparation <poc_guide/enhanced_evaluation_preparation>
    Automation <poc_guide/automation>

.. toctree::
   :caption: Infrastructure hardening
   :titlesonly:
   :maxdepth: 3

	Infrastructure Hardening <infrastructure_hardening/infrastructure_hardening>
    Segmentation using Zones <infrastructure_hardening/Hardening_Zones>
    Hardening Backup Repository - Linux <infrastructure_hardening/hardening_backup_repository_linux>
    Hardening Backup Repository - Windows <infrastructure_hardening/hardening_backup_repository_windows>

.. toctree::
   :caption: Anatomy of backup
   :titlesonly:
   :maxdepth: 3

	Backup & Replication Anatomy <anatomy/readme>
    Backup <anatomy/backup>
    VM Restore <anatomy/vm_restore>
    Instant VM Recovery <anatomy/instant_vm_recovery>
    Windows File-Level Restore <anatomy/windows_file_level_restore>
    Replication <anatomy/replication>

.. toctree::
   :caption: Networking diagrams and ports
   :titlesonly:
   :maxdepth: 3

	Networking Diagrams <networking/readme>
    Backup Server <networking/veeam_backup_server>
    Proxy Server <networking/proxy_server>
    Repository Server <networking/repository_server>
    Storage Integration <networking/storage_integration>
    Data Validation <networking/data_validation>
	Application-aware Image Processing <networking/aaip>
    Enterprise Manager <networking/veeam_backup_enterprise_manager>
    Sizing Summary <resource_planning/Appendix_A_Sizing>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
