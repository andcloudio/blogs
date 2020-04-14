# Increase Developer Productivity with skaffold

Primary focus of Developer is to write code. Build, Test and Deploy of the application are better left to be managed by tools. skaffold is an opensource tool developed by Google to help in automating some of the mundane tasks that comes with using kubernetes.

Developers go through iterative code and test cycle, that involves building container images, changing the tags of images in kubernetes yaml files and deploying the images to local kubernetes cluster.

Skaffold can help in automating these tasks, as we code and save the source files, skaffold can detect changes and initiate pipeline to build, tag and deploy application to our local or remote kubernetes cluster.

Lets take a simple hello world example and walk through the work flow.

## Required Installations:

Virtual Box: https://www.virtualbox.org/wiki/Downloads
Minikube: https://kubernetes.io/docs/tasks/tools/install-minikube/
Skaffold: https://skaffold.dev/docs/install/

## Start minikube

```bash
$ minikube start --driver=virtualbox
```

simple hello world program.

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

kubernetes yaml to deploy pod for testing.

pod.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hello-app
spec:
  containers:
  - name: hello-app
    image: hello-app
```

In skaffold configuration yaml file we specify steps to build container image using Dockerfile and deploy using pod.yaml.

skaffold.yaml

```yaml
apiVersion: skaffold/v2beta1
kind: Config
metadata:
  name: hello-app
build:
  artifacts:
  - image: hello-app
deploy:
  kubectl:
    manifests:
    - pod.yaml
```

‘skaffold dev’ command will watch an application’s source files, and when it detects changes, will rebuild your images, push any new images, and redeploy the application to your local cluster.

```bash
$ skaffold dev

Listing files to watch...
 - hello-app
Generating tags...
 - hello-app -> hello-app:302875c-dirty
Checking cache...
 - hello-app: Not found. Building
Found [minikube] context, using local docker daemon.
Building [hello-app]...
...
Successfully built cae7e96d9aa6
Successfully tagged hello-app:302875c-dirty
...
Starting deploy...
 - pod/hello-app created
```

skaffold runs the build and deploy steps.

Check the pod deployed.

```bash
$ kubectl get pod
NAME        READY   STATUS    RESTARTS   AGE
hello-app   1/1     Running   0          36s
```

Use port-forwarding to access the pod.

```bash
$ kubectl port-forward pod/hello-app 8080 &
$ curl localhost:8080
Hello World!
```

Make any change, save file. skaffold dev automatically runs build and deploy.

```bash
$ curl localhost:8080
Hello New World!
```

Now Developers can just code and test, without having to worry about editing yaml files and running commands to build and deploy application.

skaffold increases Developer productivity by automating build, tag and deploy of application to local kubernetes cluster.
