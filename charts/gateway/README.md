## Conduktor Gateway chart

A Kafka-protocol aware proxy.

## Installation

```sh
helm repo add conduktor https://helm.conduktor.io
helm repo update
helm install my-gateway conduktor/conduktor-gateway
```

## Parameters

### Gateway image configuration

This section defines the image to be used.

| Name                       | Description                                              | Value                         |
| -------------------------- | -------------------------------------------------------- | ----------------------------- |
| `gateway.image.registry`   | Docker registry to use                                   | `docker.io`                   |
| `gateway.image.repository` | Image in repository format (conduktor/conduktor-gateway) | `conduktor/conduktor-gateway` |
| `gateway.image.tag`        | Image tag                                                | `3.3.1`                       |
| `gateway.image.pullPolicy` | Kubernetes image pull policy                             | `IfNotPresent`                |

### Gateway configurations

This section contains configuration of the Conduktor Gateway.

| Name                         | Description                                                                                                                        | Value                                                                                                                                                                                                                                                                                                                       |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gateway.replicas`           | number of gateway instances to be deployed                                                                                         | `2`                                                                                                                                                                                                                                                                                                                         |
| `gateway.secretRef`          | Secret name to load sensitive env var from                                                                                         | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.extraSecretEnvVars` | Array with extra secret environment variables                                                                                      | `[]`                                                                                                                                                                                                                                                                                                                        |
| `gateway.secretSha256sum`    | Optional sha256sum of the referenced secret. This could be set to have a automactic restart of gateway deployment if secret change | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.env`                | Environment variables for Gateway deployment                                                                                       | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.interceptors`       | Json configuration for interceptors to be loaded at startup by Gateway                                                             | `[]`                                                                                                                                                                                                                                                                                                                        |
| `gateway.portRange.start`    | Start port of the gateway port range                                                                                               | `9092`                                                                                                                                                                                                                                                                                                                      |
| `gateway.portRange.count`    | Max number of broker to expose                                                                                                     | `7`                                                                                                                                                                                                                                                                                                                         |
| `gateway.admin.port`         | Admin HTTP server port                                                                                                             | `8888`                                                                                                                                                                                                                                                                                                                      |
| `gateway.jmx.enable`         | Enable JMX JVM options                                                                                                             | `false`                                                                                                                                                                                                                                                                                                                     |
| `gateway.jmx.port`           | JMX port to expose by default JVM args                                                                                             | `9999`                                                                                                                                                                                                                                                                                                                      |
| `gateway.jmx.jvmArgs`        | Arguments to pass to the gateway container JVM                                                                                     | `-Dcom.sun.management.jmxremote.port={{ .Values.gateway.jmx.port }} -Dcom.sun.management.jmxremote.rmi.port={{ .Values.gateway.jmx.port }} -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.local.only=false -Dcom.sun.management.jmxremote.ssl=false -Djava.rmi.server.hostname=127.0.0.1` |
| `gateway.startupProbeDelay`  | Optional delay in second before startup probe should be running (default 10)                                                       | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.podLabels`          | Specific labels to be added to Gateway pod by deployment                                                                           | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.podAnnotations`     | Gateway pod annotations                                                                                                            | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.securityContext`    | Container security context                                                                                                         | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.volumes`            | Define user specific volumes for Gateway deployment                                                                                | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.volumeMounts`       | Define user specific volumeMounts for Gateway container in deployment                                                              | `{}`                                                                                                                                                                                                                                                                                                                        |

### TLS configuration

This section is for configuring Gateway to handle certificate to manage TLS endpoint inside Gateway deployment.

| Name               | Description                           | Value          |
| ------------------ | ------------------------------------- | -------------- |
| `tls.enable`       | Enable TLS injection into Gateway     | `false`        |
| `tls.secretRef`    | Secret name with keystore to load     | `""`           |
| `tls.keystoreKey`  | Key in the secret to load as keystore | `keystore.jks` |
| `tls.keystoreFile` | File name to mount keystore as        | `keystore.jks` |

### Gateway service configurations

This section contains Kubernetes services configuration.


### Gateway external service configurations

This section specifies external service configuration

| Name                           | Description                                         | Value       |
| ------------------------------ | --------------------------------------------------- | ----------- |
| `service.external.enable`      | Enable a service for external connection to Gateway | `false`     |
| `service.external.type`        | Type of load balancer                               | `ClusterIP` |
| `service.external.ip`          | IP to configure                                     | `""`        |
| `service.external.annotations` |                                                     | `{}`        |
| `service.external.admin`       | Enable admin exposition on external service         | `false`     |
| `service.external.jmx`         | Enable jmx exposition on external service           | `false`     |

### Conduktor-gateway internal service configurations

This section specify internal service configuration

| Name                           | Description | Value |
| ------------------------------ | ----------- | ----- |
| `service.internal.annotations` |             | `{}`  |

### Gateway ingress configurations

This section contains Kubernetes ingress configuration.

| Name                       | Description                                                                                                                      | Value                    |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| `ingress.enabled`          | Enable ingress for Gateway                                                                                                       | `false`                  |
| `ingress.pathType`         | Ingress path type                                                                                                                | `ImplementationSpecific` |
| `ingress.apiVersion`       | Force Ingress API version (automatically detected if not set)                                                                    | `""`                     |
| `ingress.hostname`         | Default host for the ingress record                                                                                              | `gateway.local`          |
| `ingress.ingressClassName` | IngressClass that will be used to implement the Ingress (Kubernetes 1.18+)                                                       | `""`                     |
| `ingress.path`             | Default path for the ingress record                                                                                              | `/`                      |
| `ingress.annotations`      | Additional annotations for the Ingress resource. To enable certificate autogeneration, place here your cert-manager annotations. | `{}`                     |
| `ingress.tls`              | Enable TLS configuration for the host defined at `ingress.hostname` parameter                                                    | `false`                  |
| `ingress.selfSigned`       | Create a TLS secret for this ingress record using self-signed certificates generated by Helm                                     | `false`                  |
| `ingress.extraHosts`       | An array with additional hostname(s) to be covered with the ingress record                                                       | `[]`                     |
| `ingress.extraPaths`       | An array with additional arbitrary paths that may need to be added to the ingress under the main host                            | `[]`                     |
| `ingress.extraTls`         | TLS configuration for additional hostname(s) to be covered with this ingress record                                              | `[]`                     |
| `ingress.secrets`          | Custom TLS certificates as secrets                                                                                               | `[]`                     |
| `ingress.extraRules`       | Additional rules to be covered with this ingress record                                                                          | `[]`                     |

### Gateway metrics activation

Gateway embed metrics to be installed within you cluster if your have the correct capabilities (Prometheus and Grafana operators).

| Name                                     | Description                                                                      | Value                    |
| ---------------------------------------- | -------------------------------------------------------------------------------- | ------------------------ |
| `metrics.alerts.enable`                  | Enable Prometheus alerts if Prometheus alerts rules is supported on cluster      | `false`                  |
| `metrics.checklyAlerts.enable`           | Enable alerts for checky jobs if Prometheus rules is supported on cluster        | `false`                  |
| `metrics.prometheus.enable`              | Enable ServiceMonitor Prometheus operator configuration for metrics scrapping    | `false`                  |
| `metrics.prometheus.annotations`         | Additional custom annotations for the ServiceMonitor                             | `{}`                     |
| `metrics.prometheus.labels`              | Extra labels for the ServiceMonitor                                              | `{}`                     |
| `metrics.prometheus.jobLabel`            | The name of the label on the target service to use as the job name in Prometheus | `app.kubernetes.io/name` |
| `metrics.prometheus.metricRelabelings`   | Configure metric relabeling in ServiceMonitor                                    | `{}`                     |
| `metrics.prometheus.relabelings`         | Configure relabelings in ServiceMonitor                                          | `{}`                     |
| `metrics.prometheus.extraParams`         | Extra parameters in ServiceMonitor                                               | `{}`                     |
| `metrics.grafana.enable`                 | Enable Grafana dashboards to installation                                        | `false`                  |
| `metrics.grafana.labels`                 | Additional custom labels for Grafana dashboard ConfigMap                         | `{}`                     |
| `metrics.grafana.datasources.prometheus` | Prometheus datasource to use for metric dashboard                                | `prometheus`             |
| `metrics.grafana.datasources.loki`       | Loki datasource to use for log dashboard                                         | `loki`                   |

### Kubernetes common configuration

Shared Kubernetes configuration of the chart.

| Name                                          | Description                                                      | Value  |
| --------------------------------------------- | ---------------------------------------------------------------- | ------ |
| `serviceAccount.create`                       | Specifies whether a ServiceAccount should be created             | `true` |
| `serviceAccount.name`                         | The name of the ServiceAccount to use.                           | `""`   |
| `serviceAccount.annotations`                  | Additional Service Account annotations (evaluated as a template) | `{}`   |
| `serviceAccount.automountServiceAccountToken` | Automount service account token for the server service account   | `true` |
| `commonLabels`                                | Labels to be applied to all resources created by this chart      | `{}`   |
| `nodeSelector`                                | Container node selector                                          | `{}`   |
| `tolerations`                                 | Container tolerations                                            | `[]`   |
| `affinity`                                    | Container affinity                                               | `{}`   |

### Dependencies

Enable and configure chart dependencies if not available in your deployment.

| Name            | Description                                                                   | Value   |
| --------------- | ----------------------------------------------------------------------------- | ------- |
| `kafka.enabled` | Deploy a kafka along side gateway (This should only used for testing purpose) | `false` |


## Example

The following `values.yaml` file can be used to set up Gateway to proxy traffic to a Confluent Cloud cluster:

```yaml
gateway:
  env:
    # Configure connection to Confluent Cloud
    KAFKA_BOOTSTRAP_SERVERS: pkc-xxxxx.region.provider.confluent.cloud:9092
    KAFKA_SASL_MECHANISM: PLAIN
    KAFKA_SECURITY_PROTOCOL: SASL_SSL
    KAFKA_SASL_JAAS_CONFIG: org.apache.kafka.common.security.plain.PlainLoginModule required username="<your API key>" password="<your API secret>";
    # Configure Client -> Gateway
    GATEWAY_SECURITY_PROTOCOL: DELEGATED_SASL_PLAINTEXT
    # clients will be able to authenticate to Gateway with the Confluent Cloud API keys/secrets, no TLS on Gateway
  portRange:
    start: 9099
    count: 100 # to accomodate large shared (Basic or Standard) Confluent Cloud clusters
```
See [Gateway Documentation](https://docs.conduktor.io/gateway/configuration/env-variables/) for a list of environment variables that can be used.
In particular, the [Client to Gateway Authentication page](https://docs.conduktor.io/gateway/configuration/client-authentication/) details the different authentication mechanisms that can be used with Gateway.

