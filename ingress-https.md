# kubernetes + ingress + cert-manager + letsencrypt = https

If you are hosting a service in Kubernetes, want to enable https secure access to your site from outside world and want to generate certificate, free of cost, as well as want automatic management and renewal of certificate, then below details can help you.

Here we will generate certificate for the service hosted in Kubernetes using cert-manager and letsencrypt.

## Install helm client

```sh
brew install kubernetes-helm
```

## Install tiller

Tiller is Helm’s server-side component, which helm client uses to deploy resources. Tiller is given admin privileges.

```sh
kubectl create serviceaccount tiller --namespace=kube-system
kubectl create clusterrolebinding tiller-admin \
--serviceaccount=kube-system:tiller --clusterrole=cluster-admin
helm init --service-account=tiller
```

## Deploy cert-manager

```sh
kubectl apply -f https://raw.githubusercontent.com/jetstack/cert-manager/release-0.6/deploy/manifests/00-crds.yaml
kubectl create namespace cert-manager
kubectl label namespace cert-manager \
certmanager.k8s.io/disable-validation=true
helm repo update
helm install \
  --name cert-manager \
  --namespace cert-manager \
  stable/cert-manager
```

## Verify the cert-manager installation

```sh
kubectl get pods --namespace cert-manager
```

## Deploy a nginx web server

```sh
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --type=NodePort --port=80
```

## Deploy nginx ingress controller

```sh
helm install stable/nginx-ingress --name=nginx-ingress
```

## Get external IP address of loadbalancer nginx-ingress-controller

```sh
kubectl get svc
```

It will take some time for loadbalancer to get provisioned


## Create DNS entry mapping your domain name with external ip address in your DNS provider

## Create ingress resource for http access

```sh
cat << EOF | kubectl apply -f -
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: basic-ingress
spec:
  backend:
    serviceName: nginx
    servicePort: 80
EOF
```

## Point the browser to DNS name

Wait for dns propogation, it takes 5–10 minutes, we need to get ‘welcome to nginx’ html web page.

## Configure Let’s Encrypt Issuer

Edit the email address below, user@example.com to your email address to be used for ACME registration.

```sh
cat << EOF | kubectl apply -f -
apiVersion: certmanager.k8s.io/v1alpha1
kind: Issuer
metadata:
 name: letsencrypt-prod
spec:
 acme:
   # The ACME server URL
   server: https://acme-v02.api.letsencrypt.org/directory
   # Email address used for ACME registration
   email: user@example.com
   # Name of a secret used to store the ACME account private key
   privateKeySecretRef:
     name: letsencrypt-prod
   # Enable the HTTP-01 challenge provider
   http01: {}
EOF
```

## Update ingress resource to enable tls

Edit the host below, example.example.com to your dns name.

```sh
cat << EOF | kubectl apply -f -
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: basic-ingress
  annotations:
    certmanager.k8s.io/issuer: "letsencrypt-prod"
    certmanager.k8s.io/acme-challenge-type: http01
spec:
  tls:
  - hosts:
    - example.example.com
    secretName: example-tls
  rules:
  - host: example.example.com
    http:
      paths:
      - backend:
          serviceName: nginx
          servicePort: 80
EOF
```

## Check certificate is obtained from letsencrypt

```sh
kubectl get cert
```

wait for certificate status to become ready.

## Point the browser to https://\<dnsname\>

we need to see web server available on https.