# Kops

Kops provides a Production Grade K8s Installation, Upgrades, and Management. It is especially handy on AWS as you may choose to use kops instead of EKS to create kubernetes cluster on AWS.

Below are steps to create a test cluster using kops.

## Install kops binary

```sh
brew update && brew install kops
```

## Install AWS Cli

```sh
brew update && brew install awscli
```

## Setup IAM User

Create kops user with following permissions

```
AmazonEC2FullAccess
AmazonRoute53FullAccess
AmazonS3FullAccess
IAMFullAccess
AmazonVPCFullAccess
```

## Create kops user using aws cli

```sh
aws iam create-group --group-name kops

aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess --group-name kops

aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonRoute53FullAccess --group-name kops

aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --group-name kops

aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/IAMFullAccess --group-name kops

aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonVPCFullAccess --group-name kops

aws iam create-user --user-name kops

aws iam add-user-to-group --user-name kops --group-name kops

aws iam create-access-key --user-name kops

```

Record the SecretAccessKey and AccessKeyID in the returned JSON output.

configure the aws client to use your new IAM user

```sh
aws configure
```

export SecretAccessKey and AccessKeyID

```sh
export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
```

## Create S3 bucket for cluster state storage

```sh
aws s3api create-bucket \
    --bucket myfirstcluster-state-store \
    --region us-east-1
```

## Create gossip based cluster

set up environment variable for cluster name and S3 bucket used to store etcd state. For gossip cluster name must end with k8s.local

```sh
export NAME=myfirstcluster.k8s.local
export KOPS_STATE_STORE=s3://myfirstcluster-state-store
```

## Create cluster configuration

```sh
kops create cluster \
    --node-count 3 \
    --master-size t2.medium \
    --authorization RBAC \
    --networking canal \
    --zones us-east-1a \
    --ssh-public-key ~/.ssh/id_rsa.pub \
    --cloud=aws \
    --topology=private \
    --name ${NAME}
```

This creates cluster state in S3 bucket.

Create a new ssh public key called admin

```sh
kops create secret sshpublickey admin -i ~/.ssh/id_rsa.pub --name ${NAME}
```

## Build the Cluster

```sh
kops update cluster ${NAME} --yes
```

## Wait and check cluster creation

```sh
kops validate cluster
```

## check nodes and cluster components

```sh
kubectl get nodes
kubectl -n kube-system get pods
```

we have simple kops cluster to test.

## Add bastion node

To access the nodes within cluster in private topology we use bastion node


```sh
kops create instancegroup bastions --role Bastion --subnet utility-us-east-1a --name ${NAME}
```

save the file

Update the cluster

```sh
kops update cluster ${NAME} --yes
kops validate cluster
```

## Get ELB address created for bastion node

```sh
bastion_elb_url=`aws elb --output=table describe-load-balancers|grep DNSName.\*bastion|awk '{print $4}'`
```

## Use ssh-agent to access bastion

```sh
eval `ssh-agent -s`
```

Add AWS key pair .pem file

```sh
ssh-add -K <keypair>.pem
```

ssh to bastion

```sh
ssh -A admin@${bastion_elb_url}
```

ssh to master or worker nodes

```sh
ssh <master_ip>
```

## To Delete the cluster

```sh
kops delete cluster --name ${NAME} --yes
```