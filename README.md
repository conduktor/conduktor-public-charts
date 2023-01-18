![Conduktor logo](https://avatars.githubusercontent.com/u/60062294?s=200&v=4)
# Conduktor Helm Charts

## Charts

- platform-controller ([doc](platform/README.md), [values](platform/values.yaml))
- conduktor-proxy ([doc](proxy/README.md), [values](proxy/values.yaml))

## Prerequisites

- Kubernetes

#### Installing [Helm](https://helm.sh/docs/intro/install/)

## Installing Conduktor Helm Repository

```
helm repo add conduktor https://helm.conduktor.io
helm repo update
```

## Installing the Chart

Search all the repositories available
```
helm search repo conduktor -l
```

Install specific helm chart

```
helm install platform-controller conduktor/platform-controller
helm status platform-controller
```

## Uninstalling the Chart

To uninstall/delete the `platform-controller` deployment:

```
$ helm delete platform-controller
```