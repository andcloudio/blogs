# Remote Access with BeyondCorp

![Alt text](img/micah-williams-lmFJOx7hPc4-unsplash-2.jpg?raw=true "Beyond Remote Access")

Traditionally companies have relied on perimeter security with firewall guarding the entry and exit of traffic into corporate network. With companies adopting cloud and workforce going mobile, this perimeter has become difficult to enforce. 

BeyondCorp is a security model from Google, where corporate apps are moved to internet, access is based on user and device credentials, user's network location can be at enterprise location, a home network or a coffee shop, the authentication and authorization layer remains common. There is no need for traditional VPN connection.

![Alt text](img/beyond-remote-access.png?raw=true "Beyond Remote Access")

In this blog we will look varies components involved in BeyondCorp Remote Access to on-premises apps.

Building Blocks of BeyondCorp Remote Access are Cloud Identity, Cloud Identity-Aware Proxy, Context-Aware Access, Cloud IAM, Cloud Interconnect/Cloud VPN, IAP Connector and VPC Service Controls.


## User Identities

Google Cloud uses Google Accounts for authentication and access management. If there is an existing on-premises identity management system like Active Directory then usernames are synced to Cloud Identity using Google Cloud Directory Sync. Passwords are not synced, instead SAML SSO is implemented to authenticate Users with existing on-premises identity management system.

## Context-Aware access 

Access Context Manager provides granular access controls based on attributes like user identity, device type, operating system, geo-location, IP address, time of day, request path and more.

Endpoint Verification enables to build an inventory of devices that are accessing corporate apps. It provides overview of security posture of devices. 

Endpoint Verification consists of a Chrome extension installed on corporate devices. Employees can also install it on their unmanaged, personal devices. This extension gathers and reports device information, constantly syncing with Google Cloud. This information is used for finer access control.

![Alt text](img/endpoint-verification-flow.png?raw=true "endpoint-verification-flow")


## Extend on-premises network to VPC network

On-premises network is extended to Google Cloud VPC network via Dedicated Interconnect or Partner Interconnect or IPsec VPN. This provides private IP access between networks.

## Setup of Authentication and Authorization Layer

Cloud Identity-Aware Proxy(IAP) is HTTPS Load Balancer that performs authentication and authorization. User connects to this proxy to access corporate apps. Users are added as Members to HTTPS Resources in IAP, with appropriate IAM Roles to grant access. 


![Alt text](img/iap-on-prem.png?raw=true "iap-on-prem")




## Route Traffic to on-premises network

IAP Connector is used to route traffic secured by Cloud IAP to on-premises app. IAP Connector is based on Ambassador Proxy deployed on GKE cluster.

## DNS

Public domain names are created for internal on-premises app and mapped to IAP Proxy IP address.  These domain names are used by users to connect to corporate apps.


## Conclusion:

With workforce going mobile, BeyondCorp model of security provides uniform user experience between local and remote access to enterprise resources.


Diagrams from: 

https://cloud.google.com/solutions/beyondcorp-remote-access

https://cloud.google.com/endpoint-verification/docs/overview

https://cloud.google.com/iap/docs/concepts-overview

Photo by Micah Williams on Unsplash
