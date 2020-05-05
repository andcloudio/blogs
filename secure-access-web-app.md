# Secure Access to Web Apps with Identity-Aware Proxy

Identiy-Aware Proxy(IAP) is a managed service on Google Cloud, which helps to control access to apps deployed on cloud or on-premises. IAP uses User Identity and Context of the request to authenticate the user. It enables employees to connect to Enterprise Apps from any location.

Granular access control policies can be applied based on attributes like User Identity, Device Type, Geo-Location, IP address and more.

![Alt text](img/iap-2.png?raw=true "authentication")

Internet-accessible URLs are created for Enterprise Apps, DNS mapping is created for domain name to point to HTTPS Load Balancer IP address.

User connects to HTTPS Load Balancer. HTTPS Load Balancer checks if IAP is enabled for backend service. If IAP is enabled, User is redirected to Google Account Signin page. If credentials are valid, IAP checks if user is authorized to access the resource. If user has appropriate Role and Permissions, request is forwarded to backend resource.

This blogs gives an illustration of deployment of app and configuration of IAP.

```bash
PROJECT_ID="Enter project-name"

gcloud config set project ${PROJECT_ID}

gcloud services enable compute.googleapis.com
gcloud services enable container.googleapis.com
gcloud services enable iap.googleapis.com
gcloud services enable dns.googleapis.com

```

## Reserve global static ip address

```bash
gcloud compute addresses create address-name --global --ip-version IPV4
STATIC_IP=`gcloud compute addresses describe address-name --global | awk 'NR == 1 {print $2}'`
```

## Create a domain name for app in Cloud DNS

## Create 'A' record entry mapping domain name with static ip address. 

## Create a custom network and subnetwork.

```bash
REGION=us-central1
ZONE=us-central1-a
NETWORK_NAME=web-network
SUBNET_NAME=web-subnet
IP_RANGE=10.1.1.0/24

gcloud compute networks create ${NETWORK_NAME} \
--subnet-mode=custom

gcloud compute networks subnets create ${SUBNET_NAME} \
--network=${NETWORK_NAME} \
--range=${IP_RANGE} \
--region=${REGION}
```

## Create Private GKE Cluster

```bash
gcloud container clusters create cluster-name \
  --network=${NETWORK_NAME} \
  --subnetwork=${SUBNET_NAME} \
  --zone ${ZONE} \
  --cluster-version "latest" \
  --machine-type=n1-standard-4 \
  --image-type "COS" \
  --enable-autoscaling --max-nodes=5 --min-nodes=1 \
  --enable-master-authorized-networks \
  --enable-private-nodes \
  --master-ipv4-cidr "172.16.0.0/28" \
  --enable-ip-alias 
```

## Create NAT router to enable download of container images

```bash
gcloud compute routers create nat-router \
  --network=${NETWORK_NAME} \
  --region ${REGION}
  
gcloud compute routers nats create nat-config \
    --router-region ${REGION} \
    --router nat-router \
    --nat-all-subnet-ip-ranges \
    --auto-allocate-nat-external-ips
```

## Use Cloud Shell to connect to cluster

```bash
SHELL_IP=`dig +short myip.opendns.com @resolver1.opendns.com`

gcloud container clusters update cluster-name \
    --zone ${ZONE} \
    --enable-master-authorized-networks \
    --master-authorized-networks ${SHELL_IP}/32

gcloud container clusters get-credentials cluster-name \
  --zone ${ZONE} \
  --project ${PROJECT_ID}
```

## Deploy sample app on GKE

deployment.yaml

```yaml
apiVersion: v1
kind: ConfigMap
metadata:  
  name: nginx-index-html-configmap 
data:
  index.html: |  
    <!doctype html><html><body><h1>Internal Portal</h1></body></html>
---
apiVersion: v1
kind: Service
metadata:
  name: internal-portal
  labels:
    run: internal-portal
spec:
  ports:
  - port: 80
    protocol: TCP
  selector:
    run: internal-portal
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: internal-portal
spec:
  selector:
    matchLabels:
      run: internal-portal
  replicas: 2
  template:
    metadata:
      labels:
        run: internal-portal
    spec:
      containers:
      - name: internal-portal
        image: nginx
        ports:
        - containerPort: 80
        volumeMounts:
          - mountPath: /usr/share/nginx/html/index.html
            name: nginx-conf
            subPath: index.html
      volumes:
        - name: nginx-conf
          configMap:
            name: nginx-index-html-configmap

```

```bash
kubectl apply -f deployment.yaml
```

## Edge Proxy / Ingress Controller

We will use Layer 7 proxy to accept the incoming traffic and route the traffic to underlaying service. Ambassador Edge Stack is an ingress controller built on Envoy Proxy.

![Alt text](img/ambassador.png?raw=true "ambassador")

## Install Ambassador

```bash
kubectl create clusterrolebinding my-cluster-admin-binding --clusterrole=cluster-admin --user=$(gcloud info --format="value(config.account)")

kubectl apply -f https://www.getambassador.io/yaml/ambassador/ambassador-crds.yaml

kubectl apply -f https://www.getambassador.io/yaml/ambassador/ambassador-rbac.yaml
```

ingress.yaml

```yaml
apiVersion: networking.gke.io/v1beta1
kind: ManagedCertificate
metadata:
  name: www-example-com
spec:
  domains:
    - [DOMAIN NAME OF APP]
---
apiVersion: getambassador.io/v2
kind: Mapping
metadata:
  name: www-example-com
  namespace: default
spec:
  prefix: /
  service: internal-portal:80
---
apiVersion: v1
kind: Service
metadata:
  name: ambassador
spec:
  type: NodePort
  ports:
    - port: 8080
      targetPort: 8080
  selector:
    service: ambassador
---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress
  annotations:
    kubernetes.io/ingress.global-static-ip-name: address-name
    networking.gke.io/managed-certificates: www-example-com
spec:
  backend:
    serviceName: ambassador
    servicePort: 8080
```

```bash
kubectl apply -f ingress.yaml
```

## Create firewall rule to allow health check from load balancer.

```bash
FIREWALL_RULE_NAME=allow-lb
gcloud compute firewall-rules create ${FIREWALL_RULE_NAME} \
--network=${NETWORK_NAME} \
--allow=tcp \
--source-ranges=130.211.0.0/22,35.191.0.0/16 \
--description="Allow traffic from load balancer"
```

## Setup IAP

- In the Cloud Console, go to the “Security > Identity-Aware Proxy” page.

- Configure 'OAuth consent screen'. 

- Set ‘User Type’ as Internal.

- Enter Support email and Application name.

- Click Save.

## Setting up IAP access

- On the Identity-Aware Proxy page, under HTTPS Resources.

- Select the resource by checking the box to its left. On the right side panel, click Add Member.

- In the Add members dialog, add the email addresses of groups or individuals to whom you want to grant the 'IAP-secured Web App User' role for the project.

- Turning on IAP for app, with toggle slider.

![Alt text](img/iap-config.png?raw=true "iap-config")


## Test Access

- Use an incognito window in Chrome. Enter app URL, you are prompted for Google Signin. Enter credentials of authorized user. You should get access to the app.

![Alt text](img/google-signin.png?raw=true "Google signin")

![Alt text](img/access.png?raw=true "access")

- Try to access the app with an account that isn't authorized.

![Alt text](img/access-denied.png?raw=true "access denied")


## Summary

Identity-Aware proxy can give uniform authentication and authorization layer across applications without any application code.
