![Conduktor logo](https://avatars.githubusercontent.com/u/60062294?s=200&v=4)
# Conduktor Helm Charts

## Charts

- platform ([doc](https://github.com/conduktor/conduktor-public-charts/blob/main/charts/console/README.md), [values](https://github.com/conduktor/conduktor-public-charts/blob/main/charts/console/values.yaml))
- platform-controller (deprecated) ([doc](platform-controller/README.md), [values](platform-controller/values.yaml))
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

Check our [documentation](https://docs.conduktor.io/platform/configuration/env-variables/) for help.
