# SASE: Future of Enterprise Network and Network Security 

How useful is Enterprise Network and Network Security if most of the work force are working from remote location?

With less applications hosted on Enterprise Data Center and more on Public Cloud, can we still strict users to go through Enterprise Data Center to access them?  

With less Data stored in Enterprise Data Center and more in SaaS applications, where should security be focused?

Can SD-WAN take a new avatar and move from branch office to home to provide security and quality of service to where users are?

This is where Gartner paper on Secure Access Service Edge (SASE) in 2019 hype cycle comes in. SASE is about providing a cloud native converged Network and Network Security as a Service with integration of SD-WAN, SWG, CASB, FWaaS and ZTNA.

![Alt text](img/sase.png?raw=true "sase")

SASE will provide centralized, cloud based policy management with distributed enforcement points logically close to entity. Security policies can be applied dynamically based on user/device identity, geo-location, time of day, risk/trust assessment of device. 

SASE vendor will have globally distributed network fabric with network PoPs close to user. SASE can provide improved network performance by bandwidth aggregation from SD-WAN at source, optimized routing in network fabric and accelerated connection to SaaS application.


## SASE Stack

![Alt text](img/sase-stack.png?raw=true "sase")

SASE can provide continuous monitoring of user sessions. Real time DLP can be appropriately applied based on session. With Single pass architecture, inspection engine could be run in parallel instead of service chaining. 

Client agent installed on managed device or web agent on un-managed devices will help  in assessing device security posture. Local PoP will be used to provide end-to-end encryption to protect from eavesdropping.

SASE will scan SaaS application API to provide visibility into Data stored and prevent Data exfiltration by limiting access.

SASE will provide Edge computing capabilities for IoT devices. 

SASE can reduce operational complexity and cost with consolidation of varies access services into single service.

## Summary

SASE will enable optimized secure path for users to connect to services where-ever they are hosted.

Original Gartner paper can be accessed at this link.
https://www.gartner.com/doc/reprints?id=1-1OG9EZYB&ct=190903&st=sb


