# Setting up Authentication and RBAC Authorization in Kubernetes

If you want provide restricted access to a team member to work only in particular namespace in Kubernetes cluster, then we need to create authentication and role based access control (RBAC) for the user.

## Generate private key and certificate request for user — Bob

```sh
openssl genrsa -out bob.key 2048 
openssl req -new -key bob.key -out bob.csr -subj "/CN=bob"
```

## Create certificate signing request object in Kubernetes

```sh
cat <<EOF | kubectl create -f -
apiVersion: certificates.k8s.io/v1beta1
kind: CertificateSigningRequest
metadata:
  name: user-bob-csr
spec:
  groups:
  - system:authenticated
  request: $(cat bob.csr | base64 | tr -d '\n')
  usages:
  - digital signature
  - key encipherment
  - client auth
EOF
```

## Approve certificate as admin

```sh
kubectl get csr
kubectl certificate approve user-bob-csr
```

## Download user’s assigned certificate

In the below command, use base64 -D on mac or base64 -decode on linux.

```sh
kubectl get csr user-bob-csr -o jsonpath='{.status.certificate}' | base64 -D > bob.crt
```

## Create a namespace

```sh
kubectl create namespace ns-bob
```

## Authorize the user as admin inside the namespace

```sh
kubectl create rolebinding user-bob \
--clusterrole=cluster-admin --user=bob --namespace=ns-bob
```

## Generate kubeconfig for the user

```sh
APISERVER=$(kubectl config view --minify | grep server | cut -f 2- -d ":" | tr -d " ")
kubectl config set-cluster test-cluster \
  --insecure-skip-tls-verify=true \
  --server=$APISERVER \
  --kubeconfig=bob.kubeconfig
kubectl config set-credentials bob \
  --client-certificate=bob.crt \
  --client-key=bob.key \
  --embed-certs=true \
  --kubeconfig=bob.kubeconfig
kubectl config set-context bob \
  --cluster=test-cluster \
  --user=bob \
  --namespace=ns-bob \
  --kubeconfig=bob.kubeconfig
```

## Provide kubeconfig to user

Bob should be able to create deployments in namespace ns-bob

```sh
export KUBECONFIG=bob.kubeconfig
kubectl create deployment busybox --image=busybox 
kubectl get deployment,rs,pod
```

If Bob tries to use any cluster scope resource, it should be forbidden

```sh
kubectl get nodes
Error from server (Forbidden): nodes is forbidden: User "bob" cannot list nodes at the cluster scope
```

We were able to authenticate a user and give him access to a namespace.
