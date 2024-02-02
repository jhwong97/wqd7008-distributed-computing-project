# Implementation of Parallel and Distributed Compunting in Data Processing Works with HTCondor.

The following sections describe the process of replicating this project works.

## Setting Up Amazon Web Services EC2 Instances.
1. Spin up a total of four (4) EC2 Instances with the configurations stated below:
    - Instance 1:
        - Name: **CondorHost**
        - Instance Type: t2.micro
    - Instance 2:
        - Name: **SubmHost**
        - Instance Type: t2.medium
    - Instance 3:
        - Name: **Executor01**
        - Instance Type: t2.medium
    - Instance 4:
        - Name: **Executor02**
        - Instance Type: t2.medium
    
    *Notes: All EC2 instances are using   **Amazon Linux 2023 AMI**, and group under the same security group. A new key pair or existing key pair can be used to securely connect to the launched instances.*

2. Configure the inbound rules for the selected security group to allow all traffic to pass within the security pool group.
    - Navigate to the AWS EC2 sidebar, and select the **Security Groups** from the drop down list of **Network & Security**.
    - Select the used seciurity group name and edit the inbound rules.
    - Choose **All traffic** for **Type**, **Custom** for **Source**, and select the security group name in the box next to **Source**.
    - Save the configuration.

## Setting Up HTCondor Cluster
1. Access the EC2 instances and perform updates.
    - Connect to the instances via SSH client.
    - Perform update on all instances using `sudo apt-get update`.

2. Assigning HTCondor roles to each machines. In this  project, **CondorHost** is the Central Manager whereas **SubmHost** is the Submission Host. The remaining two instances - **Executor01** and **Executor02** are the Execution Hosts.
    - To assign the Central Manager, run the following command line (Refer to this [guide](https://htcondor.readthedocs.io/en/latest/getting-htcondor/admin-quick-start.html#assigning-roles-to-machines)):

        ```curl -fsSL https://get.htcondor.org|sudo GET_HTCONDOR_PASSWORD="$htcondor_password" /bin/bash -s -- --no-dry-run --central-manager $central_manager_name```
    - To assign the Submission Host, run the following command line:

        ```curl -fsSL https://get.htcondor.org | sudo GET_HTCONDOR_PASSWORD="$htcondor_password" /bin/bash -s -- --no-dry-run --submit $central_manager_name```
    - To assign the Execution Host, run the following command line:

        ```curl -fsSL https://get.htcondor.org | sudo GET_HTCONDOR_PASSWORD="$htcondor_password" /bin/bash -s -- --no-dry-run --execute $central_manager_name```
3. After installing/assigning the roles for each instance, run the following codes to check if the HTCondor is functioning properly:
    - Run
    ```sudo systemctl status condor``` command line to verify the presence of specific components within the CGroup, as per the role of the instance:
        - At Central Manager, **condor_collector** and **condor_negotiator** need to be found at CGRoup.
        - On the Submission Host, **condor_schedd** needs to be found at CGroup.
        - On the Execution Host, **condor_startd** needs to be found at CGroup.
    - If any of these components are missing according to the respective roles, execute the following commands to restart the HTCondor:
        - ```sudo systemctl enable condor```
        - ```sudo systemctl restart condor```
        - ```sudo systemctl status condor```

    - Execute the command ```condor_status``` to verify the detection of all Execution Hosts within the HTCondor cluster. If any Execution Hosts are found missing, check that all instances are configured with the same security group and confirm that they are correctly linked with the correct Central Manager IP address during the roels assigning phase.
        
    *Notes: If the above approach does not rectify the issue with missing components, consider exploring alternative troubleshooting techniques*
