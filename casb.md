# Get Visibility and Control into your SaaS Apps Usage

Today Enterprises are using different cloud service providers for IaaS, PaaS and SaaS to enhance productivity and reduce cost.

![Alt text](img/casb.png?raw=true "casb")

When using Iaas, PaaS or SaaS, Security is a shared responsibility. Service Provider is responsible for infrastructure security, User is responsible for Securing Access and Data.

How do you secure Access and Data across different service providers which are outside your enterprise perimeter?

This is where Cloud Access Security Broker (CASB) comes in. CASB acts as intermediary between users and cloud service providers. CASB helps with,

## Visibility

- Identify usage of sanctioned and un-sanctioned apps by your Employees. 

- Identify usage of Managed and Un-managed devices to access corporate data.

- Identify who has access to what resource. Get activity logs to identify who did what.

- Identify cloud services used and find redundancies. 

## Compliance

- Ensure compliance to HIPAA or HITECH for health organization, PCI for retail, FINRA for financial services organization.

## Data Security

- Identify and Classify the Data residing in SaaS applications. 

- Use DLP to identify and redact sensitive data.

- Identify Data exposed to public. Change access policies to limit exposer.

## Threat Protection

- Scan for malware. 

- Identify compromised accounts.

CASB can be deployed as 

## API Scanner

CASB can use OAUTH to scan API's provided by service provider to get resource inventory, access policies and activity logs and provide notification to IT for any usage violations.

## Forward Proxy

User connects to CASB and CASB proxies connection to SaaS applications, with this real time DLP can be applied. On corporate managed devices an endpoint agent is installed, which can control access to sanctioned and un-sanctioned applications.

## Reverse Proxy 

CASB acts as SSO agent. SaaS applications forward connections to CASB for authentication. CASB will use IDaaS used by organization to authenticate user and session is established with CASB in path between user and SaaS application. This can control access from managed and un-managed devices and provide real time DLP. 

## Conclusion

CASB provides visibility and control when using IaaS, PaaS, SaaS applications.




