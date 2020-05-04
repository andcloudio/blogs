# Setting up Development Environment on Google Cloud

Moving Development Environment to remote server on cloud provides lot of benefits.

- Secure the access to source code.

- Access to bigger compute and storage resources.

- Enables Developers to work from any location.

In this blog we will setup a development server on Google Cloud.

Below is an illustration. It containes components that are billable by Google Cloud.

## Install Cloud SDK

https://cloud.google.com/sdk/install

## Login with google account

```bash
gcloud auth login
```

## Setup following variables which we will use in gcloud commands.

```bash
PROJECT_ID=”Enter project-name"
REGION=”us-central1"
ZONE=”us-central1-a”
BILLING_ACCOUNT=”Enter your billing account number"
NETWORK_NAME=”dev-network”
SUBNET_NAME=”dev-subnet”
IP_RANGE=”10.1.1.0/24"
NAT_ROUTER=”nat-router-us-central1"
ALLOW_SSH_FROM_IAP=”allow-ssh-from-iap”
INSTANCE_NAME=”dev-vm”
NAT_CONFIG=”nat-config”
```

## Create/Set into project for Development Environment.

```bash
gcloud projects create ${PROJECT_ID}
gcloud config set project ${PROJECT_ID}
gcloud config set compute/region ${REGION}
gcloud config set compute/zone ${ZONE}
gcloud alpha billing accounts list
gcloud alpha billing projects link ${PROJECT_ID} \
--billing-account ${BILLING_ACCOUNT}
```

## Create a custom network and subnetwork.

```bash
gcloud compute networks create ${NETWORK_NAME} \
--bgp-routing-mode=global  \
--subnet-mode=custom
gcloud compute networks subnets create ${SUBNET_NAME} \
--network=${NETWORK_NAME} \
--range=${IP_RANGE} \
--region=${REGION} \
--enable-private-ip-google-access
```

## Create VM instance with no external IP address.

```bash
gcloud compute instances create ${INSTANCE_NAME} \
--network=${NETWORK_NAME} \
--subnet=${SUBNET_NAME} \
--machine-type=n1-standard-4 \
--image=ubuntu-1804-bionic-v20200317 \
--image-project=ubuntu-os-cloud \
--zone=${ZONE} \
--tags=http-tag \
--no-address \
--metadata enable-oslogin=TRUE \
--boot-disk-size=10GB \
--boot-disk-type=pd-standard \
--boot-disk-device-name=${INSTANCE_NAME} \
--no-boot-disk-auto-delete
```

## Create a NAT router instance to enable VM instance to connect to internet.

This is required to download sofware packages, access Git repositories from VM.

```bash
gcloud compute routers create ${NAT_ROUTER} \
--network ${NETWORK_NAME} \
--region ${REGION}

gcloud compute routers nats create ${NAT_CONFIG} \
--router-region ${REGION} \
--router ${NAT_ROUTER} \
--nat-all-subnet-ip-ranges \
--auto-allocate-nat-external-ips
```

## Identity-aware proxy

Identity-Aware Proxy (IAP) enables secure access to resources on cloud. IAP works by verifying user identity and context of the request to determine if a user should be allowed to access the resource. This enables developers to work from untrusted networks without the use of a VPN.

## Setup firewall rule to allow traffic from IAP on port 22.

```bash
gcloud compute firewall-rules create ${ALLOW_SSH_FROM_IAP} \
--network=${NETWORK_NAME} \
--source-ranges=35.235.240.0/20 \
--target-tags=http-tag \
--allow tcp:22
```

## Set up IAP

- In the Cloud Console, go to the “Security > Identity-Aware Proxy” page.'

- Configure OAuth consent screen. Go to the OAuth consent screen.

- Set ‘User Type’ as Internal.

- Enter Support email you want to display as a public contact.

- Enter the Application name you want to display.

- Click Save.

## Add members to the access list

- In the Cloud Console, go to the “Security > Identity-Aware Proxy” page.

- Click on tab ‘SSH AND TCP RESOURCES’

- Click on resource, Click Add member.

- Add members email address.

- Select role ‘Cloud IAP’ -> IAP-secured Tunnel User

- Click ‘Save’

## Try to ssh from Developer’s laptop

Establish ssh tunnel between VM and laptop.

```bash
gcloud compute ssh ${INSTANCE_NAME} --tunnel-through-iap
```

## Setup VS Code

We will setup VS Code to access VM remotely.

- Install remote development extension pack.

https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack

## Get ssh command

Get the internal ssh command used by ‘gcloud compute ssh’ to connect to VM, we will use this in VS code to remote-ssh.

```bash
gcloud compute ssh ${INSTANCE_NAME} --tunnel-through-iap --dry-run
/usr/bin/ssh -t -i /Users/userid/.ssh/google_compute_engine -o CheckHostIP=no -o HostKeyAlias=compute.477310433786 -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile=/Users/userid/.ssh/google_compute_known_hosts -o ProxyCommand /System/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python -S /Users/userid/google-cloud-sdk2/lib/gcloud.py compute start-iap-tunnel dev-vm %p --listen-on-stdin --project=project-id --zone=us-central1-a --verbosity=warning -o ProxyUseFdpass=no userid@compute.477310433786
```

- copy the ssh command

- remove ‘/usr/bin’ in ssh command and enclose ProxyCommand within double quotes.

```bash
ssh -t -i /Users/userid/.ssh/google_compute_engine -o CheckHostIP=no -o HostKeyAlias=compute.477310433786 -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile=/Users/userid/.ssh/google_compute_known_hosts -o ProxyCommand "/System/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python -S /Users/userid/google-cloud-sdk2/lib/gcloud.py compute start-iap-tunnel dev-vm %p --listen-on-stdin --project=project-id --zone=us-central1-a --verbosity=warning" -o ProxyUseFdpass=no userid@compute.477310433786
```

## Remote-ssh: Add new host

- Cmd + Shift + P on VS code.

- Remote-ssh: Add New Host

- Paste the ssh command, press enter.

- select configuration file /Users/<userid>/.ssh/config

## Remote-ssh: Connect host

- Cmd + Shift + P

- Remote-ssh: Connect Host

- Select Compute instance.

You should be able to connect to server. Select root folder.

You have setup Development server with VM instance, Identity-aware proxy for secure access and connected VS Code to VM instance via ssh tunnel.

## Cleanup

Deleting the project deletes all associated resources.

```bash
gcloud projects delete ${PROJECT_ID}
```
