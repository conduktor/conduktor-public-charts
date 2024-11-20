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
    <br />
    <br />
    <a href="https://github.com/conduktor/conduktor-public-charts/releases"><img alt="Gateway Release" src="https://img.shields.io/github/v/release/conduktor/conduktor-public-charts?sort=date&filter=conduktor-gateway*&logo=github&label=Gateway%20Release&color=BCFE68"></a>
    ·
    <a href="https://github.com/conduktor/conduktor-public-charts/releases"><img alt="Console Release" src="https://img.shields.io/github/v/release/conduktor/conduktor-public-charts?sort=date&filter=Console*&logo=github&label=Console%20Release&color=BCFE68"></a>
    ·
    <img alt="License" src="https://img.shields.io/github/license/conduktor/conduktor-public-charts?color=BCFE68">
    <br />
    <br />
    <a href="https://conduktor.io/"><img src="https://img.shields.io/badge/Website-conduktor.io-192A4E?color=BCFE68" alt="Scale Data Streaming With Security and Control"></a>
    ·
    <a href="https://twitter.com/getconduktor"><img alt="X (formerly Twitter) Follow" src="https://img.shields.io/twitter/follow/getconduktor?color=BCFE68"></a>
    ·
    <a href="https://conduktor.io/slack"><img src="https://img.shields.io/badge/Slack-Join%20Community-BCFE68?logo=slack" alt="Slack"></a>
</p>

## Prerequisites

- Kubernetes 1.19+
- [Helm](https://helm.sh/docs/intro/install/) 3.2.0+

## Charts

- console ([doc](charts/console/README.md), [values](charts/console/values.yaml))
- conduktor-gateway ([doc](charts/gateway/README.md), [values](charts/gateway/gateway/values.yaml))

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
- [helm](https://helm.sh/docs/intro/install/)

You can have a working cluster on your local machine with docker and k3d, 
use the Makefile target `k3d-up` to start a cluster with nginx and a postgresql
database running.

```shell
$ make helm-deps
$ make k3d-up
$ make install-dev-deps
```

*Postgresql credentials:*

```yaml
host: postgresql.conduktor
port: 5432
username: postgres
password: conduktor
name: conduktor
```

### Setup git hooks
Pre-commit git hook require to have npm or bitnami [`readme-generator`](https://github.com/bitnami/readme-generator-for-helm) installed. 

> Note: If readme-generator not installed, hook will try to install if globally using npm


```shell
$ make install-githooks
```
Now every time you commit to the project, pre-commit hook will run the readme-generator tool to synchronize changes between charts values.yaml and README.md.

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
