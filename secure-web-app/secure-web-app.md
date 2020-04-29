# Secure Access to Enterprise Apps with Identity-Aware Proxy

Identiy-Aware Proxy(IAP) is a managed service on Google Cloud, which helps to control access to apps deployed on cloud or on-premises. IAP uses User Identity and Context of the request to authenticate the user. It enables employees to connect to Enterprise Apps from any location.

Granular access control policies can be applied based on attributes like User Identity, Device Type, Geo-Location, IP address and more.

![Alt text](img/iap-1.png?raw=true "authentication")

Internet-accessible URLs are created for Enterprise Apps, DNS mapping is created for domain name and HTTPS Load Balancer IP address.

User connects to HTTPS Load Balancer. LB checks if IAP is enabled for backend service. If IAP is enabled, User is redirected to Google Account Signin. If credentials are valid, IAP checks if user is authorized to access the resource. If users have appropriate Roles and Permissions, request is forwarded to backend service.

This blogs give an illustration of deployment of apps and configuration of IAP.

```bash
PROJECT_ID="Enter project-name"
gcloud config set project ${PROJECT_ID}
```

## Create GKE Cluster

gcloud container clusters create cluster-1

## Gitclone andcloud blog repo

git clone https://github.com/andcloudio/blogs

cd blogs/secure-web-app

## Deploy sample app on GKE

```bash
kubectl apply -f deployment.yaml
```

## Deploy VM on Compute Engine

INSTANCE_NAME="finance-portal"

```bash
gcloud compute instances create ${INSTANCE_NAME} \
--no-address \
--metadata-from-file startup-script=install.sh
```

## Edge Proxy / Ingress Controller

Edge Proxy is a Layer 7 proxy that is deployed on kubernetes cluster. It accepts incoming traffic from the external load balancer and route the traffic to Kubernetes services. 

Edge proxies are configured with Kubernetes ingress resource. Ambassador Edge Stack is an ingress controller built on Envoy Proxy. External HTTPS Load Balancer will forward IAP secured traffic to Ambassador, which will route the traffic to underlaying service. 

For Service Discovery GKE provides managed DNS for resolving service names and for resolving external names. This is implemented by kube-dns, a cluster add-on that is deployed by default in all GKE clusters.

![Alt text](img/ambassador.png?raw=true "ambassador")

## Install Ambassador

```bash
kubectl create clusterrolebinding my-cluster-admin-binding --clusterrole=cluster-admin --user=$(gcloud info --format="value(config.account)")

kubectl apply -f https://www.getambassador.io/yaml/ambassador/ambassador-crds.yaml

kubectl apply -f https://www.getambassador.io/yaml/ambassador/ambassador-rbac.yaml
```

## Install Ambassador Service

```bash
kubectl apply -f ambassador-service.yaml
```

## Configure mapping

mapping.yaml

```bash
kubectl apply -f mapping.yaml
```

## Create managed certificate for domain name

```bash
kubectl apply -f cert.yaml
```

## Reserve statis address

gcloud compute addresses create ADDRESS_NAME --global --ip-version IPV4

gcloud compute addresses describe ADDRESS_NAME

## Configure Ingress to use Ambassador service

```bash
kubectl apply -f ingress.yaml
```

```bash
kubectl get ingress
```

## update DNS entry in Domain manager.

## Setup IAP

- In the Cloud Console, go to the “Security > Identity-Aware Proxy” page.

- Configure OAuth consent screen. Go to the 'OAuth Consent Screen'.

- Set ‘User Type’ as Internal.

- Enter Support email you want to display as a public contact.

- Enter the Application name you want to display.

- Click Save.

## Setting up IAP access

- On the Identity-Aware Proxy page, under HTTPS Resources.

- Select the resource by checking the box to its left. On the right side panel, click Add Member.

- In the Add members dialog, add the email addresses of groups or individuals to whom you want to grant the 'IAP-secured Web App User' role for the project.

## Turning on IAP

- On the Identity-Aware Proxy page, under HTTPS Resources.

- To turn on IAP for the app, toggle the on/off switch in the IAP column.

## Test Access

- Access the app URL from the Google Account that you added to IAP. You should have unrestricted access to the app.

- Use an incognito window in Chrome to access the app and sign in when prompted. If you try to access the app with an account that isn't authorized, you'll see a message saying that you don't have access.

