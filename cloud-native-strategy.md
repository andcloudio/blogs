# Building Cloud Native Strategy

## SPEED: The Imperative of Digital Business

With software increasingly becoming key to how users engage with businesses and how businesses innovate to stay competitive, the speed of application development and delivery is the new digital business imperative.

## What is Cloud-Native Applications?

The cloud-native approach describes a new way of developing modern applications based on cloud principles, using services and adopting processes optimized for the agility and automation of cloud computing.

When companies build and operate applications in a cloud-native fashion, they bring new ideas to market faster and respond sooner to customer demands.

## Cloud-Native Application Development and Deployment

 ![]( image img/boxes.001.jpeg) 

### Service Based Architecture

Microservices is an architectural approach to developing an application as a collection of small services; each service implements business capabilities, runs in its own process and communicates via HTTP APIs or messaging.

Each microservice can be deployed, upgraded, scaled, and restarted independent of other services in the application, typically as part of an automated system, enabling frequent updates to live applications without impacting end customers.

Applications are designed with 12-factor app principles.

![]( image img/12app.png) 

### Container-Based Infrastructure

Cloud-native applications rely on containers to achieve true application portability across different environments and infrastructure, including public, private, and hybrid.

Cloud-native applications scale horizontally, adding more capacity by simply adding more application instances.

### DevOps Processes

DevOps principles focuses on building and delivering applications collaboratively by development, quality assurance, security, IT operations, and other teams.

### SRE

SRE model brings software engineering mindset to operations with Everything as Code. Implementing SRE model can benefit both services and teams due to higher service reliability, lower operational cost, and higher-value work for the humans.

SRE team defines a service level agreement (SLA) for the uptime of a given service. The difference between the SLA and 100% uptime is the maximum allowable downtime for errors and outages. (for 99.8% availability, the allowed downtime is just over 87 minutes per month)

SRE function is empowered to push back on low-quality software.

## Continuous Integration / Continuous Delivery

Change is best when it is small and frequent, coupled with automatic testing of smaller changes and reliable rollback of bad changes reduces the risk of downtime of service.

CI establishes a consistent and automated way to build, package, and test applications. CD automates the delivery of applications package into multiple environments like Dev, QA, Staging, Production.

![]( image img/12app.png) 

Currently there are many tools evolving to provide cloud native CI/CD.

Gitlab CI/CD and GitHub Actions enable building CI/CD workflows adjacent to code repositories.

Jenkin-X based on TektonCD provides serverless build, test and deploy capability.

## Cloud Native Landscape

Visit https://github.com/cncf/landscape to view cloud native landscape

## A opinionated Cloud Native Stack:

![]( image img/stack.png) 

## Orchestration and Management

### Kubernetes

Kubernetes is a container orchestrator, that automates the deployment and life-cycle management of containerized applications. It orchestrates compute, storage, networking for workloads.

Kubernetes enables:

- Autoscale Workloads
- Blue/Green Deployments
- Fire off jobs and scheduled cronjobs
- Manage Stateless and Stateful Applications
- Provide native methods of service discovery
- Use the SAMEAPI across bare metal and EVERY cloud provider!!!

![]( image img/kubernetes01.png) 

Cluster auto-scaling is used to dynamically control number of compute instances used by cluster based on load. Authentication, Role based access control, Pod security policy and Network policies are used add the security layer for cluster.

## Cloud-Native Storage

### Rook

Rook enables Ceph storage systems to run on Kubernetes using Kubernetes primitives. With Ceph running in the Kubernetes cluster, Kubernetes applications can mount block devices and filesystems managed by Rook.

The Rook operator automates configuration of storage components and monitors the cluster to ensure the storage remains available and healthy.

Ceph CSI plugin are deployed as sidecar container in stateful pods. This enables moving stateful pods across the cluster similar to stateless application.

## Backup and Restore

### Velero

Velero gives tools to back up and restore your Kubernetes cluster resources and persistent volumes. Velero enables:

- Take backups of your cluster and restore in case of loss.
- Migrate cluster resources to other clusters.
- Replicate your production cluster to development and testing clusters.

## Networking

### Canal

Canal is just combination of network plugins Flannel and Project calico. Flannel provides the vxlan overlay network for pod communication across the nodes. Project calico can be used for implementation of network policy.

![]( image img/network.png) 

## Service Mesh

### Istio

Istio provides a uniform way to connect, secure and observe services. Istio enables:
Automatic load balancing for HTTP, gRPC, WebSocket, and TCP traffic.

- Fine-grained control of traffic behavior with rich routing rules, retries, failovers, and fault injection.

- A pluggable policy layer and configuration API supporting access controls, rate limits and quotas.

- Automatic metrics, logs, and traces for all traffic within a cluster, including cluster ingress and egress.

- Secure service-to-service communication in a cluster with strong identity-based authentication and authorization.

![]( image img/istio.png) 

## Monitoring and Alerting

### Prometheus

Prometheus is an open-source systems monitoring and alerting toolkit. It provides a multi-dimensional data model with time series data identified by metric name and key/value pairs.

The Prometheus ecosystem consists

- Prometheus server which scrapes and stores time series data
- Client libraries for instrumenting application code
- Alertmanager to handle alerts, filter and send notifications to pagerduty, email, slack.

![]( image img/prometheus.jpeg) 

## Logging

### EFK

Fluentd, Elasticsearch and Kibana are together known as “EFK stack”. Fluentd will forward logs from the individual instances in the cluster to a centralized logging backend where they are combined for higher-level reporting using ElasticSearch and Kibana.

## Distributed Tracing

### Jaeger and OpenTracing

Jaeger is open source, end-to-end distributed tracing, used to Monitor and troubleshoot transactions in complex distributed systems.

- Distributed context propagation
- Distributed transaction monitoring
- Root cause analysis
- Service dependency analysis
- Performance / latency optimization

OpenTracing provides compatible data model and instrumentation libraries in Go, Java, Node, Python and C++.

