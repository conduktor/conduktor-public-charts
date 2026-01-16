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

## Prerequisites

- Kubernetes 1.19+
- [Helm](https://helm.sh/docs/intro/install/) 3.6.0+

## Charts

- console ([doc](charts/console/README.md), [values](charts/console/values.yaml))
- conduktor-gateway ([doc](charts/gateway/README.md), [values](charts/gateway/gateway/values.yaml))

## Chart dependencies

All charts within this repository have one dependency which is `bitnami-common`. You can find the chart here: https://github.com/bitnami/charts/tree/main/bitnami/common

## Usage

```shell
$ helm repo add conduktor https://helm.conduktor.io
$ helm repo update
```

For guides and advanced help, please refer to our
[documentation](https://docs.conduktor.io/platform/installation/get-started/kubernetes),
or to our charts `README`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Development setup

**Requirements**:
- [k3d](https://k3d.io/v5.6.0/#installation)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [helm](https://helm.sh/docs/intro/install/) 3.6.0+

You can have a working cluster on your local machine with docker and k3d,
use the Makefile target `k3d-up` to start a cluster with nginx and a postgresql
database running.

```shell
# Update helm dependencies
make helm-deps

# Create local K3D cluster for test and local dev (require k3d, helm and kubectl)
make k3d-up

# Install dependencies like a Postgresql, Minio, Monitoring stack, and Kafka.
make install-dev-deps
```

*Postgresql credentials:*

```yaml
host: postgresql.conduktor
port: 5432
username: postgres
password: conduktor
name: conduktor
```

### Install charts in local K3D cluster

```shell
 # Install Conduktor Gateway chart
helm install gateway charts/gateway \
  --namespace conduktor \
  --set gateway.env.KAFKA_BOOTSTRAP_SERVERS="kafka-local-dev.conduktor.svc.cluster.local:9092"

# Install Conduktor Console chart
helm install console charts/console \
  --namespace conduktor \
  --set config.organization.name=test \
  --set config.admin.email=test@test.io \
  --set config.admin.password=testP4ss! \
  --set config.database.password=conduktor \
  --set config.database.username=postgres \
  --set 'config.database.hosts[0].host=postgresql.conduktor.svc.cluster.local' \
  --set config.database.name=conduktor
```

### Cleanup local K3D cluster

```shell
make k3d-down
```

### Setup git hooks
Pre-commit git hook require to have npm or bitnami [`readme-generator`](https://github.com/bitnami/readme-generator-for-helm) installed.

> Note: If readme-generator not installed, hook will try to install if globally using npm


```shell
make setup-hooks
```

Now every time you commit to the project, pre-commit hook will run the readme-generator tool to synchronize changes between charts values.yaml and README.md as well as checking for secrets and linting the charts.

### Re-generate chart README
You can also run [`readme-generator`](https://github.com/bitnami/readme-generator-for-helm) directly using :

```shell
$ make generate-readme
```

### Run chart tests
You need to have [chart-testing](https://github.com/helm/chart-testing) installed and a running kubernetes cluster.

```shell
# Update helm dependencies
make helm-deps
# Create local K3D cluster for test and local dev (require k3d, helm and kubectl)
make k3d-up
# Run Chart-testing tests on chart that contain changes (require chart-testing and helm)
make test-chart
# Delete K3D cluster
make k3d-down
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>
