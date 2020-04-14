# CI/CD with Cloud Build

Continous Integration and Continous Deployment (CI/CD) pipelines are designed to take the code from 'git push' to Build, Test and Deploy in production. There is a move from having a single big build server to cloud native scaleable platforms. 

Cloud Build is a managed service on Google Cloud that can be used to Build, Test and Deploy application. 

Cloud Build can import the source code from GitHub or Bitbucket, execute build as per your specification and produce artifacts such as Docker containers or Java archives.

Build steps are run in a Docker container.

We can configure builds to fetch dependencies, run unit tests, static analyses, and integration tests, and create artifacts with build tools such as docker, gradle, maven, bazel, and gulp.

We can deploy artifacts on multiple environments like Compute Engine VM instances, Google Kubernetes Engine, App Engine, Cloud Functions and Cloud Run. 

In this blog we will look into simple workflow with <b>GitHub, Cloud Build, Google Container Registry and Cloud Run.</b> 

## Enable API's in the Google Cloud Project

- Enable Cloud Build API and Cloud Run API.

## Connect GitHub repository with Google Cloud Project & Create Push Triggers

- Follow the steps from this link

https://cloud.google.com/cloud-build/docs/automating-builds/run-builds-on-github#installing_the_google_cloud_build_app

## Sample Application

app.py

```python
from flask import Flask
app = Flask('hello')

@app.route('/')
def hello():
  return "Hello World!\n"

if __name__ == '__main__':
  app.run(host = '0.0.0.0', port = 8080)
```

Dockerfile

```dockerfile
FROM python:3.7-slim
RUN pip install flask
WORKDIR /app
COPY app.py /app/app.py
ENTRYPOINT ["python"]
CMD ["/app/app.py"]
```

## Setting up continuous deployment with Cloud Build

In the build config file we specify the steps for Cloud Build. 

cloudbuild.yaml

```yaml
steps:
# build the container image
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', 'gcr.io/$PROJECT_ID/demo-app:$COMMIT_SHA', '.']
# push the container image to Container Registry
- name: 'gcr.io/cloud-builders/docker'
  args: ['push', 'gcr.io/$PROJECT_ID/demo-app:$COMMIT_SHA']
# Deploy container image to Cloud Run
- name: 'gcr.io/cloud-builders/gcloud'
  args:
  - 'run'
  - 'deploy'
  - 'demo-app'
  - '--image'
  - 'gcr.io/$PROJECT_ID/demo-app:$COMMIT_SHA'
  - '--region'
  - 'us-central1'
  - '--platform'
  - 'managed'
images:
- 'gcr.io/$PROJECT_ID/demo-app:$COMMIT_SHA'
```

In this config file we have 'demo-app' as the service name and us-central1 as the region.


## Grant Cloud Build permissions to access Cloud Run

```bash
PROJECT_NUMBER="$(gcloud projects describe ${PROJECT_ID} --format='get(projectNumber)')"

gcloud projects add-iam-policy-binding ${PROJECT_NUMBER} \
  --member=serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com \
  --role=roles/run.admin
  
gcloud iam service-accounts add-iam-policy-binding \
  ${PROJECT_NUMBER}-compute@developer.gserviceaccount.com \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"
```

## Allow unauthenticated access to demo-app service on cloud run

```bash
gcloud run services add-iam-policy-binding demo-app \
    --member="allUsers" \
    --role="roles/run.invoker" \
    --region=us-central1 \
    --platform managed
```

## commit the changes to GitHub repository.

## View build results

- In the Cloud Console, Cloud Build --> Build History menu shows information about a build's status.

- If the build is success, in Build Log we can see URL link of the deployed container. By clicking on the link we can access the deployed demo-app service.

## Summary

- Cloud Build provides a platform for continuous build, test and deploy. 

- We can keep CI/CD pipelines and deployment environment inside a single security perimeter.



