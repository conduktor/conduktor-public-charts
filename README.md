# Conduktor Helm Charts

## Charts

TODO

## Prerequisites

TODO

#### Installing [Helm](https://helm.sh)

```
curl -L https://git.io/get_helm.sh | bash
helm init
```

## Installing Conduktor Helm Repository

```
helm repo add conduktor https://conduktor.github.io/conduktor-public-charts/
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


