# Kubernetes Overview

Kubernetes is platform to run distributed systems. It is a container orchestrator. 
It basically serves four objectives
- Create an efficient deployment workflow.
- Ability to pack workloads in available infrastructure resources.
- Improve application availability by self healing.
- Abstract the underlying infrastructure so that workloads are portable.

Kubernetes is API driven, container centric system. It is one of the most active open source project with close to 2000 contributors. It is written in Go. It abstracts the cluster implementation from workloads. So applications can be written once run on any cloud provider or on-premise.

![](https://i.imgur.com/w2UupMU.png)


we can deploy on AWS, GCP, Azure or on-premise, the application remains consistent across the deployments.

## Kubernetes components
It consists of master node and sets of worker nodes. Control plane runs on master node, applications runs on worker nodes.


![](https://i.imgur.com/WJqmJvK.png)


In simple terms Kubernetes is nothing but a database fronted by API server. API server is the policy engine that sits in front of etcd, a distributed database that holds the cluster state. Controller manager is set control loops that ensure the actual state in cluster matches desired state stored in database.

Kubernetes follows declarative schema, where the user express their intent declaratively and it is upto Kubernetes to maintain intent expressed.

Scheduler assignes Pods to appropriate worker nodes. 

Kubelet is agent that runs on every node and makes sure that container are running and healthy.

Container runtime is responsible to run containers, Kubernetes supports docker, rkt, containerd or any OCI compliant implementation.

## Kubernetes Primitives
### POD
Kubernetes managers Pods rather than containers directly. Pod is wrapper over container, it represents a instance of application. It encapsulates container, storage resource, unique network IP and options that govern how container is suppose to run.

Pod can consist of single container or set of tightly coupled containers that share resources. All the containers in Pod land on same node.

Example of co-located containers can be, one container serving html web pages to outside world and a side-car container populating those html web pages. Both the container share volume.  One container writes to volume other container reads from it.

Pods are ephmeral when the node dies, Pods are scheduled for deletion. It is more common to manage Pods using a Controller.

### Relicaset Controller
Relicaset controller takes a count, and template to create Pods.

It makes sure specified number of Pods are always running on the cluster. If any node dies, Pods are rescheduled on different node.

Replicaset is managed by higher level abstration called Deployment.

### Deployment
Deployment manages the rolling out of application. When a  new version of application is to be rolled out. It creates a new Replicaset, it rolls down the Pods created by old Replicaset and rollsup the new Replicaset.

### StatefulSet
Statefullset attaches persistent storage with instance of application. It provides guarantees of ordering and provide unique ID to Pod.

It is used by applications that requires stable network ID, persistent storage, graceful deployment and termination.

Storage is either dynamically provisioned or pre-provisioned by Admin. Network ID for the Pods is provided by Headless service.

### DaemonSet
Daemonset ensures that a Pod runs on every node in cluster. Examples are log collectors and node monitoring agents.

### Job
Till now controllers were about creating applications that need to run for ever, if an instance dies, it needs to be recreated. Jobs are about tasks that need to run to completion. Job need to run till it is successfull.

### Cronjob
Cronjob creates Jobs based on schedule.

