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

### Register validating controller

First insert the CA into `caBundle` field of `validate.yml` and then apply it:
```
$ kubectl apply -f validate.yaml
```

### To-Do

* Add `bound` label validation & smart scheduling mutation web-hooks.

## Version History

* 0.1
    * Initial Release