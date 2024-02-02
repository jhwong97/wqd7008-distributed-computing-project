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