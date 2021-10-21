# Admissioner

This is a Kubernetes validation controller that checks if `env` label exist in all incoming deployment creation requests.

If you have a common cluster for both `production` & `staging` apps you can label them with `env` to know which scalable objects you can down-scale to 0.

Further steps are:

* Adding `bound` label check to smart schedule deployments on clusters deployed with inhomogeneous infrastructure nodes.
* Connect this to the `Auto Idler` project.

## Getting Started

First create `admission` namespace with:
```
$ kubectl create namespace admission
```
Then follow bellow steps.

### Build & deploy the app

Clone this repo & build image using Dockerfile in the `app` directory.

Note that you need to generate TLS certs and put `server.crt` & `server.key` in the app directory before build.

If you want to do it in local|staging environment create a self-signed cert using:
```
$ openssl req -new -key server.key -out server.csr -subj "/C=IR/ST=example/L=example/O=OrgName/OU=IT Department/CN=example.com" && \
    openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```

Then use:
```
$ docker run \
  -v ./server.crt:/app/server.crt:ro \
  -v ./server.key:/app/server.key:ro \
  admissioner:tag
```

Also for testing in KinD(or production) you can place the cert & key in `certs.yml`, then 
create it using:
```
$ kubectl apply -f certs.yml
```

Now deploy the app with:
```
$ kubectl apply -f admissioner.yml
```

### Register validating|mutating controller

First insert the CA into `caBundle` field of `validate|mutate.yml` and then apply it:
```
$ kubectl apply -f validate|mutate.yaml
```

### To-Do

* Add custom schedulers

## Version History

* 0.2
    * Add mutation webhook & configuration manifest
* 0.1
    * Initial Release