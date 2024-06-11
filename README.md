<a name="readme-top" id="readme-top"></a>

<p align="center">
  <img src="https://avatars.githubusercontent.com/u/60062294?s=200&v=4" width="256px" />
</p>
<p align="center">
    <strong>Official repository for Conduktor Helm Charts</strong>
</p>

<p align="center">
    <a href="https://docs.conduktor.io/platform/installation/get-started/kubernetes/"><strong>Explore the docs 
»</strong></a>
    <br />
    <br />
    <a href="https://github.com/conduktor/conduktor-public-charts/issues">Report Bug</a>
    ·
    <a href="https://github.com/conduktor/conduktor-public-charts/issues">Request Feature</a>
</p>

## Charts

- console ([doc](https://github.com/conduktor/conduktor-public-charts/blob/main/charts/console/README.md), [values](https://github.com/conduktor/conduktor-public-charts/blob/main/charts/console/values.yaml))
- conduktor-gateway ([doc](https://github.com/conduktor/conduktor-public-charts/blob/main/charts/gateway/README.md), [values](https://github.com/conduktor/conduktor-public-charts/blob/main/charts/gateway/values.yaml))

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
