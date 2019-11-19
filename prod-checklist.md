# The Production-Grade Infrastructure Checklist

- Install the software binaries and all dependencies. 

- Configure the software at runtime. Includes port settings, TLS certs, service discovery, leaders, followers, replication, etc.

- Provision the infrastructure. Includes servers, load balancers, network configuration, firewall settings, IAM permissions, etc.

- Deploy the service on top of the infrastructure. Roll out updates with no downtime. Includes blue-green, rolling, and canary deployments.

- Withstand outages of individual processes, servers, services, data centers, and regions.

- Scale up and down in response to load. Scale horizontally (more servers) and/or vertically (bigger servers).

- Optimize CPU, memory, disk, network, and GPU usage. Includes query tuning, benchmarking, load testing, and profiling.

- Configure static and dynamic IPs, ports, service discovery, firewalls, DNS, SSH access, and VPN access.

- Encryption in transit (TLS) and on disk, authentication, authorization, secrets management, server hardening.

- Availability metrics, business metrics, app metrics, server metrics, events, observability, tracing, and alerting.

- Rotate logs on disk. Aggregate log data to a central location.

- Make backups of DBs, caches, and other data on a scheduled basis. Replicate to separate region/account.

- Pick proper Instance types, use spot and reserved Instances, use auto scaling, and nuke unused resources.

- Document your code, architecture, and practices. Create playbooks to respond to incidents.

- Write automated tests for your infrastructure code. Run tests after every commit and nightly.
