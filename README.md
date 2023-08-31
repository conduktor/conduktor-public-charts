![Conduktor logo](https://avatars.githubusercontent.com/u/60062294?s=200&v=4)
# Conduktor Helm Charts

## Charts

- console ([doc](https://github.com/conduktor/conduktor-public-charts/blob/main/charts/console/README.md), [values](https://github.com/conduktor/conduktor-public-charts/blob/main/charts/console/values.yaml))
- platform-controller (deprecated) ([doc](platform-controller/README.md), [values](platform-controller/values.yaml))
- conduktor-proxy ([doc](proxy/README.md), [values](proxy/values.yaml))

## Prerequisites

- Kubernetes 1.19+
- Helm 3.1.0+

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

Check our kubernetes [documentation](https://docs.conduktor.io/platform/installation/get-started/kubernetes/) for help.
