# Securing Cloud Infrastructure 

- Security testing of the infrastructure should be automated as part of the CD pipeline.

## Application Deployer 

- An application container is pushed into the container repository.

- The container repository calls a webhook URL hosted by the deployer, indicating that a new version of the application container is ready for deployment.

- Upon reception of a webhook, the deployer calls Docker Hub to verify the authenticity of the notification.

- The deployer executes a series of tests against various parts of the infrastructure.

- If the tests pass, application is deployed.


## Restricting network access

- On a three-tier architecture application you need to configure each group to only accept connections from the group that precedes it.

### For Example: 

- Load balancer should accept connections from the entire internet on port 443.

- EC2 instance of the application should accept connections from the load balancer on port 80.

- Database should accept connection from the application on specific port.

- Define security groups to restrict access between tiers.

### Tools: 

- Pineapple is a network policy inspector used to perform security groups evaluation. 

## Building a secure entry point

- Create a secure entry point for debugging with bastion host

- Configure multi-factor authentication for connection to bastion host, either OTP or Push authentication.

- Configure access logs for audit trail.

- Generate an SSH key-pair, integrate with identity provider.

- Evaluate the security of the bastion’s configuration with ssh-scan.

- Mozilla’s OpenSSH guidelines maintain a modern configuration template for SSHD that can be found at https://wiki.mozilla.org/Security/Guidelines/OpenSSH.

- Disable the ssh-agent and instead use the -A flag on the SSH command line when the agent is needed.

- ProxyJump option provides a safe alternative to SSH-agent forwarding.

- open SSH access from the bastion to application tiers.

## Controlling access to the database

- Provide least priviledges to perform task on databases to application, operator or developer.

- All mature databases provide fine-grained access control and permissions

- Users that connect to a database are identified by their role. A role carries a set of permissions and can own database objects, like tables, sequences, or indexes. 

- A grant gives permission to a role to perform an operation. Standard grants are SELECT, INSERT, UPDATE, DELETE, REFERENCES, USAGE, UNDER, TRIGGER, and EXECUTE

- Limiting the permissions of the application to prevent SQL injection vulnerabilities.

- Input sanitization should have been used to escape sensitive characters.

- The application that handles student records should never have been allowed to issue a DROP statement on the database.

