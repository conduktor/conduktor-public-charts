## Conduktor gateway chart

A Kafka booster

## Installation

```
helm repo add conduktor https://helm.conduktor.io
helm repo update
helm install myGateway conduktor/conduktor-gateway
```

## Parameters

### Conduktor-gateway configurations

This section contains configuration of the gateway


### Conduktor-gateway image configuration

This section define the image to be used

| Name                         | Description                                                                                                                        | Value                                                                                                                                                                                                                                                                                                                       |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gateway.image.registry`     | Docker registry to use                                                                                                             | `docker.io`                                                                                                                                                                                                                                                                                                                 |
| `gateway.image.repository`   | Image in repository format (conduktor/conduktor-gateway)                                                                           | `conduktor/conduktor-gateway`                                                                                                                                                                                                                                                                                               |
| `gateway.image.tag`          | Image tag                                                                                                                          | `2.5.0`                                                                                                                                                                                                                                                                                                                     |
| `gateway.image.pullPolicy`   | Kubernetes image pull policy                                                                                                       | `IfNotPresent`                                                                                                                                                                                                                                                                                                              |
| `gateway.replicas`           | number of gateway instances to be deployed                                                                                         | `2`                                                                                                                                                                                                                                                                                                                         |
| `gateway.secretRef`          | Secret name to load sensitive env var from                                                                                         | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.extraSecretEnvVars` | Array with extra secret environment variables                                                                                      | `[]`                                                                                                                                                                                                                                                                                                                        |
| `gateway.secretSha256sum`    | Optional sha256sum of the referenced secret. This could be set to have a automactic restart of gateway deployment if secret change | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.env`                | Environment variables for gateway deployment                                                                                       | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.interceptors`       | Json configuration for interceptors to be loaded at startup by gateway                                                             | `[]`                                                                                                                                                                                                                                                                                                                        |
| `gateway.portRange.start`    | Start port of the gateway port range                                                                                               | `9092`                                                                                                                                                                                                                                                                                                                      |
| `gateway.portRange.count`    | Max number of broker to expose                                                                                                     | `7`                                                                                                                                                                                                                                                                                                                         |
| `gateway.admin.port`         | Admin http server port                                                                                                             | `8888`                                                                                                                                                                                                                                                                                                                      |
| `gateway.jmx.enable`         | Enable jmx jvm options                                                                                                             | `false`                                                                                                                                                                                                                                                                                                                     |
| `gateway.jmx.port`           | jmx port to expose by default jvm args                                                                                             | `9999`                                                                                                                                                                                                                                                                                                                      |
| `gateway.jmx.jvmArgs`        | arguments to pass to the gateway container jvm                                                                                     | `-Dcom.sun.management.jmxremote.port={{ .Values.gateway.jmx.port }} -Dcom.sun.management.jmxremote.rmi.port={{ .Values.gateway.jmx.port }} -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.local.only=false -Dcom.sun.management.jmxremote.ssl=false -Djava.rmi.server.hostname=127.0.0.1` |
| `gateway.startupProbeDelay`  | Optional delay in second before startup probe should be running (default 10)                                                       | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.podLabels`          | Specific labels to be added to gateway pod by deployment                                                                           | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.podAnnotations`     | gateway pod annotations                                                                                                            | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.securityContext`    | Container security context                                                                                                         | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.volumes`            | Define user specific volumes for gateway deployment                                                                                | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.volumeMounts`       | Define user specific volumeMounts  for gateway container in deployment                                                             | `{}`                                                                                                                                                                                                                                                                                                                        |

### TLS configuration

This section is for configuring gateway to handle certificate to manage SSL endpoint inside gateway deployment

| Name               | Description                           | Value          |
| ------------------ | ------------------------------------- | -------------- |
| `tls.enable`       | Enable tls injection into gateway     | `false`        |
| `tls.secretRef`    | Secret name with keystore to load     | `""`           |
| `tls.keystoreKey`  | Key in the secret to load as keystore | `keystore.jks` |
| `tls.keystoreFile` | File name to mount keystore as        | `keystore.jks` |

### Conduktor-gateway service configurations

This section contains kubernetes services configuration


### Conduktor-gateway external service configurations

This section specify external service configuration

| Name                           | Description                                         | Value       |
| ------------------------------ | --------------------------------------------------- | ----------- |
| `service.external.enable`      | Enable a service for external connection to gateway | `false`     |
| `service.external.type`        | Type of load balancer                               | `ClusterIP` |
| `service.external.ip`          | Ip to configure                                     | `""`        |
| `service.external.annotations` |                                                     | `{}`        |
| `service.external.admin`       | Enable admin exposition on external service         | `false`     |
| `service.external.jmx`         | Enable jmx exposition on external service           | `false`     |

### Conduktor-gateway internal service configurations

This section specify internal service configuration

| Name                           | Description | Value |
| ------------------------------ | ----------- | ----- |
| `service.internal.annotations` |             | `{}`  |

### Conduktor-gateway metrics activation

Gateway embed metrics to be installed within you cluster if your have the correct capabilities (Prometheus and Grafana operators)

| Name                                     | Description                                                                   | Value        |
| ---------------------------------------- | ----------------------------------------------------------------------------- | ------------ |
| `metrics.alerts.enable`                  | Enable prometheus alerts if prometheus alerts rules is supported on cluster   | `false`      |
| `metrics.checklyAlerts.enable`           | Enable alerts for checky jobs if prometheus rules is supported on cluster     | `false`      |
| `metrics.prometheus.enable`              | Enable ServiceMonitor prometheus operator configuration for metrics scrapping | `false`      |
| `metrics.prometheus.metricRelabelings`   | Configure metric relabeling in ServiceMonitor                                 | `{}`         |
| `metrics.prometheus.relabelings`         | Configure relabelings in ServiceMonitor                                       | `{}`         |
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

| Name            | Description                                                                   | Value   |
| --------------- | ----------------------------------------------------------------------------- | ------- |
| `kafka.enabled` | Deploy a kafka along side gateway (This should only used for testing purpose) | `false` |

