# Edge Security with Cloud Armor

Cloud Armor is managed service from Google Cloud used to secure web applications behind external HTTP(S) load balancers. 

Policies can be applied on external HTTP(S) load balancer to allow or deny traffic based on IP address, CIDR ranges, country code and request attributes.

cross-site scripting (XSS) and SQL injection (SQLi) attacks can be mitigated by using pre-configured rules.

![Alt text](img/armor.png?raw=true "cloud armor")

In this blog we will deploy a simple app on Google Kubernetes Engine and configure Cloud Armor.

## Create deployment in GKE

deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: default
spec:
  selector:
    matchLabels:
      run: web
  template:
    metadata:
      labels:
        run: web
    spec:
      containers:
      - image: gcr.io/google-samples/hello-app:1.0
        imagePullPolicy: IfNotPresent
        name: web
        ports:
        - containerPort: 8080
          protocol: TCP
```

```bash
kubectl apply -f deployment.yaml
```
## Create Security Policy

```bash
SECURITY_POLICY_NAME=security-policy-name

gcloud compute security-policies create ${SECURITY_POLICY_NAME} \
  --description "policy for users"
```

## Update Default Rule in Security Policy to deny traffic

```bash
gcloud compute security-policies rules update 2147483647 \
  --security-policy ${SECURITY_POLICY_NAME} \
  --action "deny-404"
```


## Define allow Security Policy Rules

```bash
gcloud compute security-policies rules create 1000 \
  --security-policy ${SECURITY_POLICY_NAME} \
  --expression "origin.region_code == 'IN' 
  && inIpRange(origin.ip, '117.198.122.0/24')
  && evaluatePreconfiguredExpr('sqli-stable')
  && evaluatePreconfiguredExpr('xss-stable')" \
  --action "allow" \
  --description "allow traffic from IN with specific CIDR, block SQLi and XSS"
```

## Creating a BackendConfig

A BackendConfig resource holds configuration information that's specific to Cloud Load Balancing.

backend-config.yaml

```yaml
apiVersion: cloud.google.com/v1beta1
kind: BackendConfig
metadata:
  name: backend-config
  namespace: default
spec:
  securityPolicy:
    name: SECURITY_POLICY_NAME
```

```bash
sed -i -e "s/SECURITY_POLICY_NAME/${SECURITY_POLICY_NAME}/g" backend-config.yaml

kubectl apply -f backend-config.yaml
```

## Create Service

service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web
  namespace: default
  annotations:
    beta.cloud.google.com/backend-config: '{"ports": {"8080":"backend-config"}}'
spec:
  ports:
  - port: 8080
    protocol: TCP
    targetPort: 8080
  selector:
    run: web
  type: NodePort
```

```bash
kubectl apply -f service.yaml
```

## Reserve global static ip address

```bash
gcloud compute addresses create address-name --global --ip-version IPV4
STATIC_IP=`gcloud compute addresses describe address-name --global | awk 'NR == 1 {print $2}'`
```

## Create ingress resource

ingress.yaml

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress
  annotations:
    kubernetes.io/ingress.global-static-ip-name: address-name
spec:
  backend:
    serviceName: web
    servicePort: 8080
```

## Test access 

Wait for ingress resource to created.

curl ${STATIC_IP}

Hello, world!
Version: 1.0.0

curl -v "${STATIC_IP}/?id=1 or 1=1"