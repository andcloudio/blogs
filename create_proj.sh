#!/bin/sh

if [[ "$#" -ne 1 ]]; then
  exit 1
fi

PROJECT_ID=$1
BILLING_ACCOUNT=`gcloud alpha billing accounts list | gawk 'FNR == 2 { print $1 }'`

gcloud projects create ${PROJECT_ID}
if [[ $? -ne 0 ]]; then 
  exit 1
fi

gcloud alpha billing projects link ${PROJECT_ID} \
--billing-account ${BILLING_ACCOUNT}
if [[ $? -ne 0 ]]; then 
  exit 1
fi

gcloud config set project ${PROJECT_ID}
if [[ $? -ne 0 ]]; then 
  exit 1
fi

#gcloud services list --available
gcloud services enable compute.googleapis.com
if [[ $? -ne 0 ]]; then 
  exit 1
fi

gcloud services enable container.googleapis.com
if [[ $? -ne 0 ]]; then 
  exit 1
fi

gcloud services enable iap.googleapis.com
if [[ $? -ne 0 ]]; then 
  exit 1
fi
