# Admissioner

This is a Kubernetes validating controller that checks if `production` label exists in all incoming deployment creation requests.

If you have a common cluster for both `production` & `staging` apps you can label them with `production` to know which scalable objects you can scale to 0.

Further steps are:

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