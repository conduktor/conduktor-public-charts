<a name="readme-top" id="readme-top"></a>

<p align="center">
  <img src="https://raw.githubusercontent.com/conduktor/conduktor.io-public/main/logo/transparent.png" width="256px" />
</p>
<h1 align="center">
    <strong>Official repository for Conduktor Helm Charts</strong>
</h1>

<p align="center">
    <a href="https://docs.conduktor.io/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/conduktor/conduktor-public-charts/issues">Report Bug</a>
    ·
    <a href="https://github.com/conduktor/conduktor-public-charts/issues">Request Feature</a>
    ·
    <a href="https://support.conduktor.io/">Contact support</a>
    <br /><br />
    <img alt="License" src="https://img.shields.io/github/license/conduktor/conduktor-public-charts?label=Charts%20license&color=BCFE68">
    <br /><br />
    <a href="https://github.com/conduktor/conduktor-public-charts/releases">
        <img alt="Console Chart Version" src="https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fconduktor%2Fconduktor-public-charts%2Frefs%2Fheads%2Fmain%2Fcharts%2Fconsole%2FChart.yaml&query=%24.version&prefix=conduktor-console:&logo=helm&label=Console%20Chart&color=BCFE68&">
    </a> /
    <a href="https://hub.docker.com/r/conduktor/conduktor-console">
        <img alt="Console Application Version" src="https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fconduktor%2Fconduktor-public-charts%2Frefs%2Fheads%2Fmain%2Fcharts%2Fconsole%2FChart.yaml&query=%24.appVersion&prefix=conduktor%2Fconduktor-console%3A&logo=docker&label=Console%20Application&color=BCFE68">
    </a>
    <br />
    <a href="https://github.com/conduktor/conduktor-public-charts/releases">
        <img alt="Gateway Chart Version" src="https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fconduktor%2Fconduktor-public-charts%2Frefs%2Fheads%2Fmain%2Fcharts%2Fgateway%2FChart.yaml&query=%24.version&prefix=conduktor-gateway:&logo=helm&label=Gateway%20Chart&color=BCFE68&">
    </a>  /
    <a href="https://hub.docker.com/r/conduktor/conduktor-gateway">
        <img alt="Gateway Application Version" src="https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fconduktor%2Fconduktor-public-charts%2Frefs%2Fheads%2Fmain%2Fcharts%2Fgateway%2FChart.yaml&query=%24.appVersion&prefix=conduktor%2Fconduktor-gateway%3A&logo=docker&label=Gateway%20Application&color=BCFE68">
    </a>
    <br /><br />
    <a href="https://conduktor.io/"><img src="https://img.shields.io/badge/Website-conduktor.io-192A4E?color=BCFE68" alt="Scale Data Streaming With Security and Control"></a>
    ·
    <a href="https://twitter.com/getconduktor"><img alt="X (formerly Twitter) Follow" src="https://img.shields.io/twitter/follow/getconduktor?color=BCFE68"></a>
    ·
    <a href="https://conduktor.io/slack"><img src="https://img.shields.io/badge/Slack-Join%20Community-BCFE68?logo=slack" alt="Slack"></a>
</p>

## Charts

- console ([doc](https://github.com/conduktor/conduktor-public-charts/blob/main/charts/console/README.md), [values](https://github.com/conduktor/conduktor-public-charts/blob/main/charts/console/values.yaml))
- conduktor-gateway ([doc](https://github.com/conduktor/conduktor-public-charts/blob/main/charts/gateway/README.md), [values](https://github.com/conduktor/conduktor-public-charts/blob/main/charts/gateway/values.yaml))

## Prerequisites

- Kubernetes 1.19+
- Helm 3.1.0+

## Chart dependencies

All charts within this repository have one dependency which is `bitnami-common`. You can find the chart here: https://github.com/bitnami/charts/tree/main/bitnami/common

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
