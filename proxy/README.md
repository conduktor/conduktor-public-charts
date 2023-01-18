## Conduktor proxy chart

A Kafka booster

## Installation

```
helm repo add conduktor https://helm.conduktor.io
helm repo update
helm install myProxy conduktor/proxy
```

## Parameters

### Conduktor-proxy configurations

This section contains configuration of the proxy




### Conduktor-proxy image configuration

This section define the image to be used

| Name                        | Description                                                          | Value                                                                                                                                                                                                                                                                                                                   |
| --------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `proxy.image.registry`      | Docker registry to use                                               | `docker.io`                                                                                                                                                                                                                                                                                                             |
| `proxy.image.repository`    | Image in repository format (conduktor/conduktor-proxy)               | `conduktor/conduktor-proxy`                                                                                                                                                                                                                                                                                             |
| `proxy.image.tag`           | Image tag                                                            | `1.0.0-amd64`                                                                                                                                                                                                                                                                                                           |
| `proxy.image.pullPolicy`    | Kubernetes image pull policy                                         | `IfNotPresent`                                                                                                                                                                                                                                                                                                          |
| `proxy.replicas`            | number of proxy instances to be deployed                             | `2`                                                                                                                                                                                                                                                                                                                     |
| `proxy.secretRef`           | Secret name to load sensitive env var from                           | `""`                                                                                                                                                                                                                                                                                                                    |
| `proxy.env`                 | Environment variables for proxy deployment                           | `{}`                                                                                                                                                                                                                                                                                                                    |
| `proxy.interceptors`        | Json configuration for interceptors to be loaded at startup by proxy | `[]`                                                                                                                                                                                                                                                                                                                    |
| `proxy.rocksDbSharedLibDir` | Folder to load rocksdb shared lib from                               | `/app/resources`                                                                                                                                                                                                                                                                                                        |
| `proxy.portRange.start`     | Start port of the proxy port range                                   | `9092`                                                                                                                                                                                                                                                                                                                  |
| `proxy.portRange.end`       | End port (inclusive) of the proxy port range                         | `9099`                                                                                                                                                                                                                                                                                                                  |
| `proxy.admin.port`          | Admin http server port                                               | `8888`                                                                                                                                                                                                                                                                                                                  |
| `proxy.jmx.enable`          | Enable jmx jvm options                                               | `false`                                                                                                                                                                                                                                                                                                                 |
| `proxy.jmx.port`            | jmx port to expose by default jvm args                               | `9999`                                                                                                                                                                                                                                                                                                                  |
| `proxy.jmx.jvmArgs`         | arguments to pass to the proxy container jvm                         | `-Dcom.sun.management.jmxremote.port={{ .Values.proxy.jmx.port }} -Dcom.sun.management.jmxremote.rmi.port={{ .Values.proxy.jmx.port }} -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.local.only=false -Dcom.sun.management.jmxremote.ssl=false -Djava.rmi.server.hostname=127.0.0.1` |
| `proxy.prometheus.port`     | Prometheus metric port                                               | `9089`                                                                                                                                                                                                                                                                                                                  |
| `proxy.podLabels`           | Specific labels to be added to proxy pod by deployment               | `{}`                                                                                                                                                                                                                                                                                                                    |
| `proxy.podAnnotations`      | Proxy pod annotations                                                | `{}`                                                                                                                                                                                                                                                                                                                    |
| `proxy.securityContext`     | Container security context                                           | `{}`                                                                                                                                                                                                                                                                                                                    |


### TLS configuration

This section is for configuring proxy to handle certificate to manage SSL endpoint inside proxy deployment

| Name               | Description                           | Value          |
| ------------------ | ------------------------------------- | -------------- |
| `tls.enable`       | Enable tls injection into proxy       | `false`        |
| `tls.secretRef`    | Secret name with keystore to load     | `""`           |
| `tls.keystoreKey`  | Key in the secret to load as keystore | `keystore.jks` |
| `tls.keystoreFile` | File name to mount keystore as        | `keystore.jks` |


### Conduktor-proxy service configurations

This section contains kubernetes services configuration




### Conduktor-proxy external service configurations

This section specify external service configuration

| Name                           | Description                                       | Value       |
| ------------------------------ | ------------------------------------------------- | ----------- |
| `service.external.enable`      | Enable a service for external connection to proxy | `false`     |
| `service.external.type`        | Type of load balancer                             | `ClusterIP` |
| `service.external.ip`          | Ip to configure                                   | `""`        |
| `service.external.annotations` |                                                   | `{}`        |
| `service.external.admin`       | Enable admin exposition on external service       | `false`     |
| `service.external.jmx`         | Enable jmx exposition on external service         | `false`     |
| `service.external.prometheus`  | Enable prometheus exposition on external service  | `false`     |


### Conduktor-proxy internal service configurations

This section specify internal service configuration

| Name                           | Description | Value |
| ------------------------------ | ----------- | ----- |
| `service.internal.annotations` |             | `{}`  |


### Conduktor-proxy metrics activation

Proxy embed metrics to be installed within you cluster if your have the correct capabilities (Prometheus and Grafana operators)

| Name                                     | Description                                                                   | Value        |
| ---------------------------------------- | ----------------------------------------------------------------------------- | ------------ |
| `metrics.alerts.enable`                  | Enable prometheus alerts if prometheus alerts rules is supported on cluster   | `false`      |
| `metrics.checklyAlerts.enable`           | Enable alerts for checky jobs if prometheus rules is supported on cluster     | `false`      |
| `metrics.prometheus.enable`              | Enable ServiceMonitor prometheus operator configuration for metrics scrapping | `false`      |
| `metrics.grafana.enable`                 | Enable grafana dashboards to installation                                     | `false`      |
| `metrics.grafana.datasources.prometheus` | Prometheus datasource to use for metric dashboard                             | `prometheus` |
| `metrics.grafana.datasources.loki`       | Loki datasource to use for log dashboard                                      | `loki`       |


### Kubernetes common configuration

Shared kubernetes configuration of the chart

| Name                    | Description                                                    | Value   |
| ----------------------- | -------------------------------------------------------------- | ------- |
| `serviceAccount.create` | Create Kubernetes service account. Default kube value if false | `false` |
| `commonLabels`          | Labels to be applied to all ressources created by this chart   | `{}`    |
| `nodeSelector`          | Container node selector                                        | `{}`    |
| `tolerations`           | Container tolerations                                          | `[]`    |
| `affinity`              | Container affinity                                             | `{}`    |


### Dependencies

Enable and configure chart dependencies if not available in your deployment

| Name            | Description                                                                 | Value   |
| --------------- | --------------------------------------------------------------------------- | ------- |
| `kafka.enabled` | Deploy a kafka along side proxy (This should only used for testing purpose) | `false` |

