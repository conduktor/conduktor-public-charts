## Conduktor Gateway chart

A Kafka-protocol aware proxy.

See our [compatibility matrix](https://docs.conduktor.io/gateway/get-started/kubernetes/#helm-chart-compatibility)

## Installation

```sh
helm repo add conduktor https://helm.conduktor.io
helm repo update
helm install my-gateway conduktor/conduktor-gateway
```

## Table of contents
* [Parameters](#parameters)
  * [Global parameters](#global-parameters)
  * [Common parameters](#common-parameters)
  * [Gateway image configuration](#gateway-image-configuration)
  * [Gateway configurations](#gateway-configurations)
  * [TLS configuration](#tls-configuration)
  * [Gateway service configurations](#gateway-service-configurations)
  * [Gateway external service configurations](#gateway-external-service-configurations)
  * [Conduktor-gateway internal service configurations](#conduktor-gateway-internal-service-configurations)
  * [Gateway ingress configurations](#gateway-ingress-configurations)
  * [Gateway metrics activation](#gateway-metrics-activation)
  * [Kubernetes common configuration](#kubernetes-common-configuration)
* [Example](#example)

## Parameters

### Global parameters

Global Docker image parameters
Please, note that this will override the image parameters, including dependencies, configured to use the global value
Current available global Docker image parameters: imageRegistry, imagePullSecrets and storageClass

| Name                      | Description                                | Value |
| ------------------------- | ------------------------------------------ | ----- |
| `global.imageRegistry`    | Global Docker image registry               | `""`  |
| `global.imagePullSecrets` | Docker login secrets name for image pull   | `[]`  |
| `global.env`              | The environment name (deprecated not used) | `""`  |

### Common parameters

| Name                | Description                                       | Value           |
| ------------------- | ------------------------------------------------- | --------------- |
| `nameOverride`      | String to partially override common.names.name    | `""`            |
| `fullnameOverride`  | String to fully override common.names.fullname    | `""`            |
| `namespaceOverride` | String to fully override common.names.namespace   | `""`            |
| `commonLabels`      | Labels to add to all deployed objects             | `{}`            |
| `commonAnnotations` | Annotations to add to all deployed objects        | `{}`            |
| `clusterDomain`     | Kubernetes cluster domain name                    | `cluster.local` |
| `extraDeploy`       | Array of extra objects to deploy with the release | `[]`            |

### Gateway image configuration

This section defines the image to be used.

| Name                       | Description                                              | Value                         |
| -------------------------- | -------------------------------------------------------- | ----------------------------- |
| `gateway.image.registry`   | Docker registry to use                                   | `docker.io`                   |
| `gateway.image.repository` | Image in repository format (conduktor/conduktor-gateway) | `conduktor/conduktor-gateway` |
| `gateway.image.tag`        | Image tag                                                | `3.20.0`                      |
| `gateway.image.pullPolicy` | Kubernetes image pull policy                             | `IfNotPresent`                |

### Gateway configurations

This section contains configuration of the Conduktor Gateway.

| Name                                         | Description                                                                                                                                                                                                                            | Value                                                                                                                                                                                                                                                                                                                       |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gateway.replicas`                           | number of gateway instances to be deployed                                                                                                                                                                                             | `2`                                                                                                                                                                                                                                                                                                                         |
| `gateway.secretRef`                          | Secret name to load sensitive env var from                                                                                                                                                                                             | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.extraSecretEnvVars`                 | Array with extra secret environment variables                                                                                                                                                                                          | `[]`                                                                                                                                                                                                                                                                                                                        |
| `gateway.secretSha256sum`                    | Optional sha256sum of the referenced secret. This could be set to have a automactic restart of gateway deployment if secret change                                                                                                     | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.env`                                | Environment variables for Gateway deployment in the form of a map of string key/value pairs                                                                                                                                            | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.licenseKey`                         | License key to activate Conduktor Gateway not used if `gateway.secretRef` is set                                                                                                                                                       | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.userPool.secretKey`                 | Secret key (256bits) encoded in base64 to sign service accounts credentials when `SASL_PLAIN` or `SASL_SSL` is used for `GATEWAY_SECURITY_PROTOCOL`. If empty, a random key will be generated. Not used if `gateway.secretRef` is set. | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.interceptors`                       | Deprecated: Json configuration for interceptors to be loaded at startup by Gateway. Use API instead. This will be removed in future versions.                                                                                          | `[]`                                                                                                                                                                                                                                                                                                                        |
| `gateway.portRange.start`                    | start port of the gateway port range (single listener mode)                                                                                                                                                                            | `9092`                                                                                                                                                                                                                                                                                                                      |
| `gateway.portRange.count`                    | max number of brokers to expose (single listener mode)                                                                                                                                                                                 | `7`                                                                                                                                                                                                                                                                                                                         |
| `gateway.admin.port`                         | Admin HTTP server port                                                                                                                                                                                                                 | `8888`                                                                                                                                                                                                                                                                                                                      |
| `gateway.admin.users[0].username`            | API Admin username. (not used if `gateway.secretRef` is set)                                                                                                                                                                           | `admin`                                                                                                                                                                                                                                                                                                                     |
| `gateway.admin.users[0].password`            | API Admin password. If empty, a random password will be generated (not used if `gateway.secretRef` is set)                                                                                                                             | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.admin.users[0].admin`               | API user admin role flag. (not used if `gateway.secretRef` is set)                                                                                                                                                                     | `true`                                                                                                                                                                                                                                                                                                                      |
| `gateway.admin.mainAdminSecretKeys.username` | Secret key used to store the username of the main admin user from `gateway.admin.users` (first with admin role)                                                                                                                        | `GATEWAY_ADMIN_USERNAME`                                                                                                                                                                                                                                                                                                    |
| `gateway.admin.mainAdminSecretKeys.password` | Secret key used to store the password of the main admin user from `gateway.admin.users` (first with admin role)                                                                                                                        | `GATEWAY_ADMIN_PASSWORD`                                                                                                                                                                                                                                                                                                    |
| `gateway.admin.securedMetrics`               | Enable secured metrics using api users credentials. If `gateway.secretRef` is set, this can't be used by `metrics.prometheus` to automatically configure basic auth on scrapping.                                                      | `true`                                                                                                                                                                                                                                                                                                                      |
| `gateway.jmx.enable`                         | Enable JMX JVM options                                                                                                                                                                                                                 | `false`                                                                                                                                                                                                                                                                                                                     |
| `gateway.jmx.port`                           | JMX port to expose by default JVM args                                                                                                                                                                                                 | `9999`                                                                                                                                                                                                                                                                                                                      |
| `gateway.jmx.jvmArgs`                        | Arguments to pass to the gateway container JVM                                                                                                                                                                                         | `-Dcom.sun.management.jmxremote.port={{ .Values.gateway.jmx.port }} -Dcom.sun.management.jmxremote.rmi.port={{ .Values.gateway.jmx.port }} -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.local.only=false -Dcom.sun.management.jmxremote.ssl=false -Djava.rmi.server.hostname=127.0.0.1` |

### Multi-listeners mode (preview)

Opt-in multi-listeners API (Gateway >= v3.18). Enable with gateway.preview.listeners: true.
When active, gateway.listeners.internal and gateway.listeners.external drive all listener
env var generation instead of the single listener gateway.portRange config. Inactive by
default — existing installs are unaffected until opt-in.

| Name                                               | Description                                                                                                                                                                                                              | Value             |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------- |
| `gateway.preview.listeners`                        | Enable experimental multi-listeners mode. When true, gateway.listeners.internal/external drive all env var generation; when false (default), single listener portRange config is used.                                   | `false`           |
| `gateway.securityMode`                             | Gateway security mode: GATEWAY_MANAGED or KAFKA_MANAGED. Only used when gateway.preview.listeners is true. Emitted as GATEWAY_SECURITY_MODE (gateway.env.GATEWAY_SECURITY_MODE takes precedence if set).                 | `GATEWAY_MANAGED` |
| `gateway.aclEnabled`                               | Enable ACL for the Gateway virtual cluster. Only used when gateway.preview.listeners is true. Emitted as GATEWAY_ACL_ENABLED. Inferred from securityMode when empty (true for GATEWAY_MANAGED, false for KAFKA_MANAGED). | `""`              |
| `gateway.kafka.brokerIds`                          | Kafka broker IDs used for SNI routing. Required when any listener uses routing: sni. Supports range syntax e.g. ["0-2"] or ["0-2,10,12-13"].                                                                             | `[]`              |
| `gateway.listeners.internal.securityProtocol`      | Listener security protocol: PLAINTEXT, SSL, SASL_PLAINTEXT or SASL_SSL                                                                                                                                                   | `PLAINTEXT`       |
| `gateway.listeners.internal.routing`               | Listener routing mode: port or sni                                                                                                                                                                                       | `port`            |
| `gateway.listeners.internal.ports`                 | Port specs. Format: ADVERTISED:LOCAL or range (e.g. "9092-9098", "443:9092")                                                                                                                                             | `["9092-9098"]`   |
| `gateway.listeners.internal.sslClientAuth`         | TLS client authentication: NONE, OPTIONAL or REQUIRE (only for SSL/SASL_SSL)                                                                                                                                             | `NONE`            |
| `gateway.listeners.external.securityProtocol`      | Listener security protocol: PLAINTEXT, SSL, SASL_PLAINTEXT or SASL_SSL                                                                                                                                                   | `SASL_SSL`        |
| `gateway.listeners.external.routing`               | Listener routing mode: port or sni                                                                                                                                                                                       | `sni`             |
| `gateway.listeners.external.ports`                 | Port specs. Format: ADVERTISED:LOCAL or range (e.g. "9092", "443:9092")                                                                                                                                                  | `["9092"]`        |
| `gateway.listeners.external.advertisedHost`        | Externally-reachable hostname. Required when preview.listeners and service.external.enable are both true.                                                                                                                | `""`              |
| `gateway.listeners.external.advertisedHostPattern` | Per-broker hostname pattern for SNI routing. Must contain {{nodeId}}.                                                                                                                                                    | `""`              |
| `gateway.listeners.external.bootstrapHostPattern`  | Bootstrap hostname for SNI routing. Derived from advertisedHostPattern if empty.                                                                                                                                         | `""`              |
| `gateway.listeners.external.sslClientAuth`         | TLS client authentication: NONE, OPTIONAL or REQUIRE (only for SSL/SASL_SSL)                                                                                                                                             | `NONE`            |

### Gateway pod/container configuration

Resource requests/limits, pod labels, security context, volumes, sidecars, init containers and health probes.

| Name                                         | Description                                                                                                                              | Value   |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `gateway.resources.limits.cpu`               | CPU limit for the platform container                                                                                                     | `2000m` |
| `gateway.resources.limits.memory`            | Memory limit for the container                                                                                                           | `4Gi`   |
| `gateway.resources.requests.cpu`             | CPU resource requests                                                                                                                    | `500m`  |
| `gateway.resources.requests.memory`          | Memory resource requests                                                                                                                 | `500Mi` |
| `gateway.podLabels`                          | Specific labels to be added to Gateway pod by deployment                                                                                 | `{}`    |
| `gateway.podAnnotations`                     | Gateway pod annotations                                                                                                                  | `{}`    |
| `gateway.securityContext`                    | Conduktor Gateway container Security Context                                                                                             | `{}`    |
| `gateway.volumes`                            | Define user specific volumes for Gateway deployment                                                                                      | `[]`    |
| `gateway.volumeMounts`                       | Define user specific volumeMounts for Gateway container in deployment                                                                    | `[]`    |
| `gateway.sidecars`                           | Add additional sidecar containers to run into the Conduktor Gateway pod(s)                                                               | `[]`    |
| `gateway.initContainers`                     | Add additional init containers to the Conduktor Gateway pod(s). ref: https://kubernetes.io/docs/concepts/workloads/pods/init-containers/ | `[]`    |
| `gateway.terminationGracePeriodSeconds`      | Duration in seconds the pod needs to terminate gracefully.                                                                               | `30`    |
| `gateway.priorityClassName`                  | Define Gateway pods' priority based on an existing ClassName                                                                             | `""`    |
| `gateway.customStartupProbe`                 | Custom startup probe configuration                                                                                                       | `{}`    |
| `gateway.startupProbe.enabled`               | Enable startupProbe on Conduktor Gaterway containers                                                                                     | `true`  |
| `gateway.startupProbe.initialDelaySeconds`   | Initial delay seconds for startupProbe                                                                                                   | `10`    |
| `gateway.startupProbe.periodSeconds`         | Period seconds for startupProbe                                                                                                          | `10`    |
| `gateway.startupProbe.timeoutSeconds`        | Timeout seconds for startupProbe                                                                                                         | `1`     |
| `gateway.startupProbe.failureThreshold`      | Failure threshold for startupProbe                                                                                                       | `5`     |
| `gateway.startupProbe.successThreshold`      | Success threshold for startupProbe                                                                                                       | `1`     |
| `gateway.customLivenessProbe`                | Custom liveness probe configuration                                                                                                      | `{}`    |
| `gateway.livenessProbe.enabled`              | Enable livenessProbe on Conduktor Gaterway containers                                                                                    | `true`  |
| `gateway.livenessProbe.initialDelaySeconds`  | Initial delay seconds for livenessProbe                                                                                                  | `0`     |
| `gateway.livenessProbe.periodSeconds`        | Period seconds for livenessProbe                                                                                                         | `5`     |
| `gateway.livenessProbe.timeoutSeconds`       | Timeout seconds for livenessProbe                                                                                                        | `1`     |
| `gateway.livenessProbe.failureThreshold`     | Failure threshold for livenessProbe                                                                                                      | `3`     |
| `gateway.livenessProbe.successThreshold`     | Success threshold for livenessProbe                                                                                                      | `1`     |
| `gateway.customReadinessProbe`               | Custom readiness probe configuration                                                                                                     | `{}`    |
| `gateway.readinessProbe.enabled`             | Enable readinessProbe on Conduktor Gaterway containers                                                                                   | `true`  |
| `gateway.readinessProbe.initialDelaySeconds` | Initial delay seconds for readinessProbe                                                                                                 | `0`     |
| `gateway.readinessProbe.periodSeconds`       | Period seconds for readinessProbe                                                                                                        | `5`     |
| `gateway.readinessProbe.timeoutSeconds`      | Timeout seconds for readinessProbe                                                                                                       | `1`     |
| `gateway.readinessProbe.failureThreshold`    | Failure threshold for readinessProbe                                                                                                     | `3`     |
| `gateway.readinessProbe.successThreshold`    | Success threshold for readinessProbe                                                                                                     | `1`     |

### TLS configuration

This section is for configuring Gateway to handle certificate to manage TLS endpoint inside Gateway deployment.

| Name                                       | Description                                                                                                                                                                                                                                                                                       | Value            |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| `tls.enable`                               | Enable TLS injection into Gateway                                                                                                                                                                                                                                                                 | `false`          |
| `tls.secretRef`                            | DEPRECATED: use tls.keystore.secretRef instead. Secret name with keystore to load                                                                                                                                                                                                                 | `""`             |
| `tls.keystoreKey`                          | DEPRECATED: use tls.keystore.keystoreKey instead. Key in the secret to load as keystore                                                                                                                                                                                                           | `keystore.jks`   |
| `tls.keystoreFile`                         | DEPRECATED: use tls.keystore.keystoreFile instead. File name to mount keystore as                                                                                                                                                                                                                 | `keystore.jks`   |
| `tls.keystore.secretRef`                   | Secret containing the JKS keystore file                                                                                                                                                                                                                                                           | `""`             |
| `tls.keystore.keystoreKey`                 | Key in the keystore secret                                                                                                                                                                                                                                                                        | `keystore.jks`   |
| `tls.keystore.keystoreFile`                | Filename to mount the keystore as                                                                                                                                                                                                                                                                 | `keystore.jks`   |
| `tls.keystore.passwordSecretRef.name`      | Secret containing the keystore password (optional; leave empty to set via gateway.env or gateway.extraSecretEnvVars)                                                                                                                                                                              | `""`             |
| `tls.keystore.passwordSecretRef.key`       | Key in the password secret                                                                                                                                                                                                                                                                        | `password`       |
| `tls.truststore.secretRef`                 | Secret containing the JKS truststore file (manual path; leave empty to skip)                                                                                                                                                                                                                      | `""`             |
| `tls.truststore.keystoreKey`               | Key in the truststore secret                                                                                                                                                                                                                                                                      | `truststore.jks` |
| `tls.truststore.keystoreFile`              | Filename to mount the truststore as (also used for cert-manager truststore path)                                                                                                                                                                                                                  | `truststore.jks` |
| `tls.truststore.passwordSecretRef.name`    | Secret containing the truststore password (optional)                                                                                                                                                                                                                                              | `""`             |
| `tls.truststore.passwordSecretRef.key`     | Key in the truststore password secret                                                                                                                                                                                                                                                             | `password`       |
| `tls.certManager.enabled`                  | Enable cert-manager integration using native JKS keystore generation (requires cert-manager >= 0.15)                                                                                                                                                                                              | `false`          |
| `tls.certManager.issuerRef.name`           | cert-manager Issuer or ClusterIssuer name                                                                                                                                                                                                                                                         | `""`             |
| `tls.certManager.issuerRef.kind`           | Issuer kind — Issuer or ClusterIssuer                                                                                                                                                                                                                                                             | `ClusterIssuer`  |
| `tls.certManager.issuerRef.group`          | Issuer group (leave empty to default to cert-manager.io)                                                                                                                                                                                                                                          | `""`             |
| `tls.certManager.extraDnsNames`            | Additional DNS SANs beyond those auto-derived from listener config                                                                                                                                                                                                                                | `[]`             |
| `tls.certManager.extraIpAddresses`         | Additional IP SANs to include in the certificate                                                                                                                                                                                                                                                  | `[]`             |
| `tls.certManager.duration`                 | Certificate validity duration. Defaults to 90 days.                                                                                                                                                                                                                                               | `2160h`          |
| `tls.certManager.renewBefore`              | How early cert-manager starts renewing before expiry. Must be less than duration.                                                                                                                                                                                                                 | `360h`           |
| `tls.certManager.sslContextRefreshMinutes` | How often Gateway reloads the SSL context from disk (GATEWAY_SSL_UPDATE_CONTEXT_INTERVAL_MINUTES)                                                                                                                                                                                                 | `5`              |
| `tls.certManager.truststore.enabled`       | Mount the cert-manager JKS truststore and set GATEWAY_SSL_TRUST_STORE_* env vars. Enable only when the upstream Kafka broker uses SSL or when Gateway listeners require mTLS. Leave false when upstream Kafka is PLAINTEXT — enabling with PLAINTEXT Kafka will cause Gateway to fail at startup. | `false`          |
| `tls.certManager.httpsAdminApi.enabled`    | Secure the admin API with the same JKS keystore                                                                                                                                                                                                                                                   | `false`          |

### Gateway service configurations

This section contains Kubernetes services configuration.


### Gateway external service configurations

This section specifies external service configuration

| Name                           | Description                                              | Value       |
| ------------------------------ | -------------------------------------------------------- | ----------- |
| `service.external.enable`      | Enable a service for external connection to Gateway      | `false`     |
| `service.external.type`        | Type of load balancer                                    | `ClusterIP` |
| `service.external.ip`          | IP to configure                                          | `""`        |
| `service.external.annotations` |                                                          | `{}`        |
| `service.external.labels`      | Labels to be added to Gateway internal service           | `{}`        |
| `service.external.admin`       | Enable admin exposition on external service              | `false`     |
| `service.external.jmx`         | Enable jmx exposition on external service                | `false`     |
| `service.external.extraSpecs`  | Extra specs for the service to be added under `spec` key | `{}`        |

### Conduktor-gateway internal service configurations

This section specify internal service configuration

| Name                           | Description                                              | Value |
| ------------------------------ | -------------------------------------------------------- | ----- |
| `service.internal.annotations` |                                                          | `{}`  |
| `service.internal.labels`      | Labels to be added to Gateway internal service           | `{}`  |
| `service.internal.extraSpecs`  | Extra specs for the service to be added under `spec` key | `{}`  |

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

| Name                                     | Description                                                                                                                                                                        | Value                        |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| `metrics.alerts.enable`                  | Enable Prometheus alerts if Prometheus alerts rules are supported on cluster                                                                                                       | `false`                      |
| `metrics.prometheus.enable`              | Enable ServiceMonitor Prometheus operator configuration for metrics scrapping                                                                                                      | `false`                      |
| `metrics.prometheus.annotations`         | Additional custom annotations for the ServiceMonitor                                                                                                                               | `{}`                         |
| `metrics.prometheus.labels`              | Extra labels for the ServiceMonitor                                                                                                                                                | `{}`                         |
| `metrics.prometheus.scheme`              | Protocol scheme to use for scraping (http or https). By default, automatically resolved based on container TLS configuration.                                                      | `""`                         |
| `metrics.prometheus.tlsConfig`           | TLS configuration for the ServiceMonitor. By default, configured to skip TLS validation.                                                                                           | `{}`                         |
| `metrics.prometheus.jobLabel`            | The name of the label on the target service to use as the job name in Prometheus                                                                                                   | `app.kubernetes.io/instance` |
| `metrics.prometheus.metricRelabelings`   | Configure metric relabeling in ServiceMonitor                                                                                                                                      | `{}`                         |
| `metrics.prometheus.relabelings`         | Configure relabelings in ServiceMonitor                                                                                                                                            | `{}`                         |
| `metrics.prometheus.extraParams`         | Extra parameters in ServiceMonitor. See https://prometheus-operator.dev/docs/api-reference/api/#monitoring.coreos.com/v1.Endpoint                                                  | `{}`                         |
| `metrics.grafana.enable`                 | Enable Grafana dashboards to installation. Dashboards can be installed as Sidecar ConfigMap or using Grafana operator CRDs (v4 or v5)                                              | `false`                      |
| `metrics.grafana.namespace`              | Namespace used to deploy Grafana dashboards by default use the same namespace as Conduktor Gateway                                                                                 | `""`                         |
| `metrics.grafana.matchLabels`            | Label selector for Grafana instance (for grafana-operator v5 only)                                                                                                                 | `{}`                         |
| `metrics.grafana.labels`                 | Additional custom labels for Grafana dashboard ConfigMap. Used by Sidecar ConfigMap loading https://github.com/grafana/helm-charts/tree/main/charts/grafana#sidecar-for-dashboards | `{}`                         |
| `metrics.grafana.folder`                 | Grafana dashboard folder name                                                                                                                                                      | `""`                         |
| `metrics.grafana.datasources.prometheus` | Prometheus datasource to use for metric dashboard                                                                                                                                  | `prometheus`                 |
| `metrics.grafana.datasources.loki`       | Loki datasource to use for log dashboard                                                                                                                                           | `loki`                       |

### Kubernetes common configuration

Shared Kubernetes configuration of the chart.

| Name                                          | Description                                                                                                                                                                                                                                                                      | Value                    |
| --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| `serviceAccount.create`                       | Specifies whether a ServiceAccount should be created                                                                                                                                                                                                                             | `true`                   |
| `serviceAccount.name`                         | The name of the ServiceAccount to use.                                                                                                                                                                                                                                           | `""`                     |
| `serviceAccount.annotations`                  | Additional Service Account annotations (evaluated as a template)                                                                                                                                                                                                                 | `{}`                     |
| `serviceAccount.automountServiceAccountToken` | Automount service account token for the server service account                                                                                                                                                                                                                   | `true`                   |
| `nodeSelector`                                | Container node selector                                                                                                                                                                                                                                                          | `{}`                     |
| `tolerations`                                 | Container tolerations                                                                                                                                                                                                                                                            | `[]`                     |
| `affinity.nodeAffinity`                       | Gateway pods node affinity configuration                                                                                                                                                                                                                                         | `{}`                     |
| `affinity.podAffinity`                        | Gateway pods affinity configuration                                                                                                                                                                                                                                              | `{}`                     |
| `affinity.podAntiAffinity`                    | Gateway pods anti-affinity configuration                                                                                                                                                                                                                                         | `{}`                     |
| `affinity.podAntiAffinityPreset.enable`       | Enable predefined pod anti-affinity presets that spread pods across nodes. If `affinity.podAntiAffinity` is set, this will be ignored. If both `affinity.podAntiAffinityPreset.enable` is `false` and `affinity.podAntiAffinity` is empty, no pod anti-affinity will be applied. | `true`                   |
| `affinity.podAntiAffinityPreset.topologyKey`  | Topology key to use for pod anti-affinity preset (default: "kubernetes.io/hostname"). If `affinity.podAntiAffinity` is set, this will be ignored.                                                                                                                                | `kubernetes.io/hostname` |
| `podSecurityContext`                          | Conduktor Gateway Pod Security Context                                                                                                                                                                                                                                           | `{}`                     |


## Example

* [Expose the Gateway](#expose-the-gateway)
  * [Two protocols, two mechanisms](#two-protocols-two-mechanisms)
  * [Component reference](#component-reference)
  * [External service types](#external-service-types)
  * [Decision guide](#decision-guide)
* [How to provide secrets](#how-to-provide-secrets)
  * [Provide you own secret with `gateway.secretRef`](#provide-you-own-secret-with-gatewaysecretref)
  * [Using `gateway.extraSecretEnvVars`](#using-gatewayextrasecretenvvars)
  * [Using values and generated secrets](#using-values-and-generated-secrets)
  * [Pulling from private registry using `global.imagePullSecrets`](#pulling-from-private-registry-using-globalimagepullsecrets)
  * [Air-gapped deployment](#air-gapped-deployment)
* [Ingress configuration examples](#ingress-configuration-examples)
  * [Nginx Ingress without TLS](#nginx-ingress-without-tls)
  * [Nginx Ingress with Self-signed TLS](#nginx-ingress-with-self-signed-tls)
  * [Nginx Ingress with Let's Encrypt TLS](#nginx-ingress-with-lets-encrypt-tls)
  * [Nginx Ingress with Custom TLS secret](#nginx-ingress-with-custom-tls-secret)
* [Provide Extra Certificates](#provide-extra-certificates)
* [Set Gateway Container and Pod Security Context](#set-gateway-container-and-pod-security-context)
* [Monitoring](#monitoring)
  * [Prometheus metrics](#prometheus-metrics)
    * [Prometheus alerts](#prometheus-alerts)
  * [Grafana dashboards](#grafana-dashboards)
    * [Sidecar ConfigMap loading](#sidecar-configmap-loading)
    * [Import dashboards manually](#import-dashboards-manually)
* [Extra resource to deploy](#extra-resource-to-deploy)
* [Multi-listeners](#multi-listeners)
  * [Port spec format](#port-spec-format)
  * [Internal-only listener (port routing)](#internal-only-listener-port-routing)
  * [Internal + external listener (SNI routing for external access)](#internal--external-listener-sni-routing-for-external-access)
  * [Internal listener with SNI routing](#internal-listener-with-sni-routing)
  * [cert-manager TLS (automated certificate management)](#cert-manager-tls-automated-certificate-management)
    * [Internal SNI routing with cert-manager](#internal-sni-routing-with-cert-manager)
    * [Internal port routing with cert-manager and secured admin API](#internal-port-routing-with-cert-manager-and-secured-admin-api)
    * [Internal + external SNI routing with cert-manager](#internal--external-sni-routing-with-cert-manager)
    * [Using a custom Issuer namespace or group](#using-a-custom-issuer-namespace-or-group)
    * [Providing a custom password secret](#providing-a-custom-password-secret)

The following `values.yaml` file can be used to set up Gateway to proxy traffic to a Confluent Cloud cluster:

```yaml file=values.yaml
gateway:
  licenseKey: "<your license key>" # set GATEWAY_LICENSE_KEY secret env var
  admin:
    users: # generate GATEWAY_ADMIN_API_USERS secret env var
      - username: admin
        password: "<your admin password>" # if empty, a random password will be generated
        admin: true
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

### Expose the Gateway

Gateway speaks two different protocols, and each one is exposed through a different Kubernetes mechanism. Understanding this split is the key to picking the right component.

#### Two protocols, two mechanisms

- **Kafka protocol** is raw TCP with per-broker routing. Every broker has to be individually addressable, and the address Gateway advertises has to resolve from the client's location. An HTTP Ingress cannot carry this traffic, so Kafka is always exposed through a Kubernetes **Service**.
- **Admin REST API** is plain HTTP, served on the `admin-http` port (`8888`). It can be exposed through a Service or through an **Ingress**.

#### Component reference

| Component | Enabled by | Exposes | Protocol |
| --------- | ---------- | ------- | -------- |
| Internal service | Always created | Kafka broker ports and `admin-http` | Kafka and HTTP |
| External service | `service.external.enable: true` | Kafka broker ports, and `admin-http` if `service.external.admin: true` | Kafka and HTTP |
| Ingress | `ingress.enabled: true` | Admin REST API only, routed to the internal service `admin-http` port | HTTP |

#### External service types

When you need to reach Gateway from outside the cluster over Kafka, set `service.external.enable: true` and choose a `service.external.type`:

- **`LoadBalancer`** (recommended): provisions an external load balancer through your cloud provider, giving Gateway a stable endpoint that is reachable from outside the cluster and that balances traffic across the Gateway pods. The actual load balancer implementation depends on your Kubernetes provider or infrastructure.
- **`NodePort`**: opens a port on every Kubernetes node, so clients reach Gateway through a node IP and that port.

We recommend `LoadBalancer` because it gives clients a single, stable external endpoint without tying them to node IPs, and it is the standard way to expose a service to external Kafka clients.

> [!NOTE]
> With multi-listeners mode, enabling SNI routing on the internal listener creates several internal `ClusterIP` services, one per hostname Gateway listens on. See [Multi-listeners](#multi-listeners) for details.

#### Decision guide

| You need to reach Gateway from | Protocol | Use |
| ------------------------------ | -------- | --- |
| Inside the cluster | Kafka | Internal service |
| Outside the cluster | Kafka | External service (LoadBalancer) |
| Inside the cluster | Admin REST API | Internal service |
| Outside the cluster | Admin REST API | Ingress |

### How to provide secrets

Some environment variables require sensitive information, such as API keys, passwords or license key. These should be provided as Kubernetes secrets.

This chart provide several ways to provide secrets to Gateway deployment:

#### Provide you own secret with `gateway.secretRef`

You can create a secret in your Kubernetes cluster and reference it in the `gateway.secretRef` field in the `values.yaml` file.

> [!IMPORTANT]
> This secret should contain **environment variables** that Gateway will use and need to be created in the same namespace as the Gateway deployment.

> [!WARNING]
> When using `gateway.secretRef`, the following will be ignored as they are expected in the `gateway.secretRef` : `gateway.licenseKey`, `gateway.admin.users` and `gateway.userPool.secretKey`.
> You should provide them in the secret using environment variable keys: `GATEWAY_LICENSE_KEY`, `GATEWAY_ADMIN_API_USERS`, `GATEWAY_USER_POOL_SECRET_KEY` respectively.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: gateway-custom-secret
type: Opaque
data:
  GATEWAY_LICENSE_KEY: <base64 encoded license key>
  GATEWAY_USER_POOL_SECRET_KEY: <base64 encoded secret key (256bits string)>
  GATEWAY_ADMIN_API_USERS: <base64 encoded admin users json>
  KAFKA_SASL_JAAS_CONFIG: <base64 encoded SASL JAAS config>
  #... other sensitive env vars
```
And then reference it in the `values.yaml` file:
```yaml file=values.yaml
gateway:
  secretRef: gateway-custom-secret
```

#### Using `gateway.extraSecretEnvVars`

You can also reference per-secret value in the `values.yaml` file directly. This is useful when using an existing secrets with different keys.

```yaml file=custom-secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: existing-kafka-secret
type: Opaque
data:
  jaas-config.properties: <base64 encoded SASL JAAS config>
  #... other sensitive config
---
apiVersion: v1
kind: Secret
metadata:
  name: existing-gateway-secret
type: Opaque
data:
  license: <base64 encoded license key>
  user-pool-secret: <base64 encoded secret key (256bits string)>
  #... other sensitive config
```

and then reference them in the `values.yaml` file:
```yaml file=values.yaml
gateway:
  extraSecretEnvVars:
    - name: GATEWAY_LICENSE_KEY
      valueFrom:
        secretKeyRef:
          name: existing-gateway-secret
          key: license
    - name: GATEWAY_USER_POOL_SECRET_KEY
      valueFrom:
        secretKeyRef:
          name: existing-gateway-secret
          key: user-pool-secret
    - name: KAFKA_SASL_JAAS_CONFIG
      valueFrom:
        secretKeyRef:
          name: existing-kafka-secret
          key: jaas-config.properties
```

> [!NOTE]
> In this example gateway chart will create a secret with only `GATEWAY_ADMIN_API_USERS` key with value from `gateway.admin.users` field
> as `GATEWAY_LICENSE_KEY` and `GATEWAY_USER_POOL_SECRET_KEY` are provided in the `gateway.extraSecretEnvVars` field.

#### Using values and generated secrets

If you don't want to create a secret, you can provide the sensitive information directly in the `values.yaml` file.
This is useful for testing or when you don't want to manage secrets in your cluster but it's not recommended for production.

```yaml file=values.yaml
gateway:
  licenseKey: "<your license key>" # set GATEWAY_LICENSE_KEY secret env var
  admin:
    users: # generate GATEWAY_ADMIN_API_USERS secret env var
      - username: admin
        password: "<your admin password>" # if empty, a random password will be generated
        admin: true
  userPool:
    secretKey: "<256bits long string>" # if empty, a random key will be generated
```


#### Pulling from private registry using `global.imagePullSecrets`

The method of setting up your private registry will work with the following registries:
- Artifactory
- Harbor
- Nexus
- GitHub Container Registry (GHCR)
- Google Container Registry (GCR)

**This method WILL NOT work for AWS Elastic Container Registry (ECR) due to it requiring an authentication token that expires every 12 hours**

To use the parameter `global.imagePullSecrets` you need to create a secret with the name you want to use in the parameter. To find out more [see offical documentation](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/).

We need to ensure this secret is of type `docker-registry` and contains the following keys:
```bash
kubectl create secret docker-registry <SECRET_NAME> \
  --docker-server=<DOCKER_REGISTRY_SERVER> \
  --docker-username=<DOCKER_USERNAME> \
  --docker-password=<DOCKER_PASSWORD> \
  --docker-email=<DOCKER_EMAIL>
```

Then in your `values.yaml` file, you can set the `global.imagePullSecrets` parameter to the name of the secret you created, you will also need to modify the `gateway.image` parameters to use the same registry as the secret you created.

The below example shows how to set the `global.imagePullSecrets` parameter and the `gateway.image` parameters to use a private registry:
```yaml
global:
  imagePullSecrets:
    - name: docker-regsitry-secret

gateway:
  image:
    registry: regsitry.company.io
    repository: conduktor/conduktor-gateway
    tag: nightly
```

#### Air-gapped deployment

To deploy Gateway in an environment without internet access, you need to complete the following steps on an internet-connected machine before deploying to the cluster.

**1. Get the chart**

Download the packaged chart from the [GitHub releases page](https://github.com/conduktor/conduktor-public-charts/releases) or pull it from the Helm repository:

```sh
helm repo add conduktor https://helm.conduktor.io
helm repo update
helm pull conduktor/conduktor-gateway --version <version>
```

Both sources ship with all chart dependencies already bundled — no `helm dependency build` needed.

**2. Repackage the chart for your private registry**

Inject your private registry as the default and push the chart to your internal OCI registry:

```sh
# Set your private image registry as the default
yq -i '.global.imageRegistry = "<your-private-registry>"' conduktor-gateway/values.yaml

# Repackage and push to your internal OCI registry
tar czf conduktor-gateway-<version>.tgz conduktor-gateway/
helm push conduktor-gateway-<version>.tgz oci://<your-chart-registry>
```

**3. Mirror the Gateway image**

Pull the Gateway image from Docker Hub and push it to your private registry:

```sh
docker pull conduktor/conduktor-gateway:<version>
docker tag conduktor/conduktor-gateway:<version> <your-private-registry>/conduktor/conduktor-gateway:<version>
docker push <your-private-registry>/conduktor/conduktor-gateway:<version>
```

**4. Set up registry authentication**

Configure your cluster to authenticate to your private registry. The recommended approach is to use your cloud provider's native registry authentication (for example, IRSA on EKS) to avoid managing short-lived credentials. Alternatively, use `global.imagePullSecrets` — see [Pulling from private registry using `global.imagePullSecrets`](#pulling-from-private-registry-using-globalimagepullsecrets).

**5. Install**

```sh
helm install my-gateway oci://<your-chart-registry>/conduktor-gateway --version <version>
```

### Ingress configuration examples

#### Nginx Ingress without TLS

**values.yaml** :
```yaml
ingress:
  enabled: true
  ingressClassName: "nginx"
  hostname: conduktor-gateway.mycompany.com
  tls: false
  selfSigned: false
```

#### Nginx Ingress with Self-signed TLS

**values.yaml** :
```yaml
ingress:
  enabled: true
  ingressClassName: "nginx"
  hostname: conduktor-gateway.mycompany.com
  tls: true
  selfSigned: true
```

#### Nginx Ingress with Let's Encrypt TLS

**values.yaml** :
```yaml
ingress:
  enabled: true
  ingressClassName: "nginx"
  hostname: conduktor-gateway.mycompany.com
  tls: true
  selfSigned: false
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    kubernetes.io/ingress.class: nginx
```

#### Nginx Ingress with Custom TLS secret

**values.yaml** :
```yaml
ingress:
  enabled: true
  ingressClassName: "nginx"
  hostname: conduktor-gateway.mycompany.com
  tls: true
  selfSigned: false
  secrets:
    - name: my-tls-secret
      certificate: |
        -----BEGIN CERTIFICATE-----
        ...
        -----END CERTIFICATE-----
      key: |
        -----BEGIN RSA PRIVATE KEY-----
        ...
        -----END RSA PRIVATE KEY-----
```

### Provide Extra Certificates
*NOTE:* The example is for a `truststore` but the same technique could be applied if you need to configure a `keystore`.

It's recommended to load your certificates as secrets.
```shell
kubectl create secret generic gateway-cert \
    --from-file=./my.truststore
```

We can then proceed to mount the secret as a volume.
Note the `mountPath` which is where our cert will be accessible from.

```yaml
gateway:
  volumes:
    - name: truststore
      secret:
        secretName: gateway-cert
        items:
        - key: kafka.truststore.jks
          path: kafka.truststore.jks
  volumeMounts:
    - name: truststore
      mountPath: /etc/gateway/tls/truststore/
      readOnly: true
```

Finally, we can configure our truststore location
```yaml
gateway:
  env:
    KAFKA_SSL_TRUSTSTORE_LOCATION: /etc/gateway/tls/truststore/kafka.truststore.jks
```

### Set Gateway Container and Pod Security Context
You can set the security context for the Gateway container and pod using the `gateway.securityContext` and `podSecurityContext` parameters.

```yaml

gateway:
  securityContext:
    capabilities:
      drop:
        - ALL
    runAsNonRoot: true
    runAsUser: 1000

podSecurityContext:
  runAsNonRoot: true
```

> [!NOTE]
> If you set `gateway.securityContext.readOnlyRootFilesystem: true`, you need to add and mount an extra volume/volumeMount to `/tmp` in the Gateway container using `gateway.volumes` and `gateway.volumeMounts`.

### Node affinity

By default, Gateway pods are configured with a pod anti-affinity that spread pods across nodes using `kubernetes.io/hostname` node label.
You can disable this behavior by setting `affinity.podAntiAffinityPreset.enable` to `false` and not setting `affinity.podAntiAffinity`.

```yaml
affinity:
  podAntiAffinityPreset: # preset ignored if affinity.podAntiAffinity is set
    enable: false
    topologyKey: "kubernetes.io/hostname"
```

### Monitoring

#### Prometheus metrics
Conduktor Gateway exposes metrics on the `/api/metrics` endpoint that can be scraped by Prometheus.

The Conduktor Gateway chart can be configured to install Prometheus [ServiceMonitor CRD](https://prometheus-operator.dev/docs/api-reference/api/#monitoring.coreos.com/v1.ServiceMonitor) from [Prometheus Operator](https://prometheus-operator.dev/) to scrape metrics if the API `monitoring.coreos.com/v1/ServiceMonitor` is available on the Kubernetes Cluster.

To enable Prometheus scraping, set the following values in your `values.yaml`:
```yaml
metrics:
  prometheus:
    enable: true
    jobLabel: app.kubernetes.io/instance # Default label used to identify the job
    #annotations: {} # Additional custom annotations for the ServiceMonitor
    #labels: {} # Extra labels for the ServiceMonitor
    #metricRelabelings: {} # Configure metric relabeling in ServiceMonitor
    #relabelings: {} # Configure relabelings in ServiceMonitor
    #extraParams: {} # Extra parameters in ServiceMonitor. See https://prometheus-operator.dev/docs/api-reference/api/#monitoring.coreos.com/v1.Endpoint
```

##### Prometheus alerts
Some default alerts are provided in the [`gateway-alerts.yaml`](./prometheus-alerts/gateway-alerts.yaml) file that make use of [PrometheusRule CRD](https://prometheus-operator.dev/docs/api-reference/api/#monitoring.coreos.com/v1.PrometheusRule).

To enable alerts, set the following values in your `values.yaml`:
```yaml
metrics:
  alerts:
    enable: true
```

#### Grafana dashboards
The Conduktor Gateway chart can be configured to install Grafana dashboards using [Grafana Operator](https://grafana.github.io/grafana-operator/).

The chart supports CRD Dashboard API v4 ([`integreatly.org/v1alpha1/GrafanaDashboard`](https://github.com/grafana/grafana-operator/blob/v4/documentation/dashboards.md)) and v5 ([`grafana.integreatly.org/v1beta1/GrafanaDashboard`](https://grafana.github.io/grafana-operator/docs/dashboards/)).

To enable Grafana dashboards, set the following values in your `values.yaml`:
```yaml
metrics:
  grafana:
    enable: true
    namespace: "" # Namespace used to deploy Grafana dashboards by default use the same namespace as Conduktor Gateway
    #matchLabels: {} # Label selector for Grafana instance (for grafana-operator v5 only)
    #labels: {} # Additional custom labels for Grafana dashboard ConfigMap. Used by Sidecar ConfigMap loading
    #folder: ""
    #datasources:
      #prometheus: prometheus  # Prometheus datasource name to use for metric dashboard
      #loki: loki # Loki datasource name to use for log dashboard (not required by main dashboard)
```

The chart then installs the Grafana dashboards as ConfigMap in the configured namespace. And init CRD if they are installed in Kubernetes Cluster.

##### Sidecar ConfigMap loading
If you are not using the Grafana Operator but an official [Grafana Helm chart](https://github.com/grafana/helm-charts/tree/main/charts/grafana), you can use the Sidecar provisioning to load dashboards from ConfigMap.

To enable Sidecar ConfigMap loading, set the following values in your `values.yaml`:
```yaml
metrics:
  grafana:
    enable: true
    namespace: "" # Namespace used to deploy Grafana dashboards by default use the same namespace as Conduktor Gateway
    labels:
      grafana_dashboard: "1" # Label to enable Sidecar ConfigMap loading check Grafana chart sidecar.dashboards.label value for expected value
```

##### Import dashboards manually
If you want to import dashboards manually, you can use the exported json files from the [grafana-dashboards](./grafana-dashboards) folder.

> [!NOTE]
> Grafana Dashboard exported json files expect to have a datasource named `prometheus` and `loki` to be available in Grafana and that Conduktor Gateway run inside Kubernetes with `pod` label on metrics.
> Dashboards are tested with Grafana **9.x** and **10.x**.


### Extra resource to deploy

You can deploy extra resources with the Gateway deployment by adding them to the `extraDeploy` field in the `values.yaml` file.

```yaml
extraDeploy:
  - apiVersion: v1
    kind: ConfigMap
    metadata:
      name: extra-configmap
    data:
      some-key: some-value
```

### With init container

You can use an init container to perform some actions before the Gateway container starts. This can be useful to prepare the environment or to run some scripts.

```yaml
gateway:
  volumes:
    - name: init-volume
      emptyDir: {}
  initContainers:
    - name: init-container
      image: busybox
      command: ["sh", "-c", "echo 'Init container running'"]
      volumeMounts:
        - name: init-volume
          mountPath: /mnt/init
```

### With sidecar container
You can add a sidecar container to the Gateway deployment to run additional processes alongside the Gateway container. This can be useful for logging, monitoring, or other purposes.

```yaml
gateway:
  volumes:
    - name: sidecar-volume
      emptyDir: {}
  sidecars:
    - name: sidecar-container
      image: busybox
      command: ["sh", "-c", "while true; do echo 'Sidecar container running'; sleep 10; done"]
      volumeMounts:
        - name: sidecar-volume
          mountPath: /mnt/sidecar
```

### Multi-listeners

Multi-listeners mode gives explicit control over listener configuration through dedicated internal and external listeners instead of the single listener port-range approach. Enable with `gateway.preview.listeners: true`.

> [!WARNING]
> This is a preview feature. The API may change in future releases.

#### Port spec format

Ports are expressed as specs in the `gateway.listeners.*.ports` list:

| Format | Example | Meaning |
|--------|---------|---------|
| Single port | `"9092"` | Advertised 9092, local 9092 |
| Port range | `"9092-9098"` | Advertised 9092–9098, local 9092–9098 |
| Mapped port | `"443:9092"` | Advertised 443, local 9092 |
| Mapped range | `"443-445:9092-9094"` | Advertised 443–445, local 9092–9094 |

#### Internal-only listener (port routing)

The simplest configuration exposes a single internal listener using port-based routing. Kafka clients inside the cluster connect to the internal ClusterIP service.

```yaml
gateway:
  preview:
    listeners: true
  securityMode: "GATEWAY_MANAGED"
  aclEnabled: "false"
  listeners:
    internal:
      securityProtocol: PLAINTEXT
      routing: port
      ports:
        - "9092-9098"
  env:
    KAFKA_BOOTSTRAP_SERVERS: kafka.default.svc.cluster.local:9092
```

#### Internal + external listener (SNI routing for external access)

This configuration adds an external LoadBalancer listener using SNI routing, which multiplexes multiple brokers over a single port. A TLS certificate covering the advertised hostnames is required.

```yaml
gateway:
  preview:
    listeners: true
  securityMode: "GATEWAY_MANAGED"
  listeners:
    internal:
      securityProtocol: PLAINTEXT
      routing: port
      ports:
        - "19092-19098"
    external:
      securityProtocol: SASL_SSL
      routing: sni
      ports:
        - "9092"
      advertisedHost: "kafka.example.com"
      advertisedHostPattern: "broker-{{nodeId}}.kafka.example.com"
      bootstrapHostPattern: "bootstrap.kafka.example.com"
  env:
    KAFKA_BOOTSTRAP_SERVERS: kafka.default.svc.cluster.local:9092

tls:
  enable: true
  secretRef: gateway-tls-secret
  keystoreKey: keystore.jks
  keystoreFile: keystore.jks

service:
  external:
    enable: true
    type: LoadBalancer
```

DNS records required for external SNI:
- `bootstrap.kafka.example.com` → LoadBalancer IP
- `*.kafka.example.com` → LoadBalancer IP (wildcard, for per-broker routing)

TLS certificate must include SANs: `*.kafka.example.com`, `bootstrap.kafka.example.com`.

#### Internal listener with SNI routing

Internal SNI routing multiplexes multiple broker addresses over a single port within the cluster. The chart creates one ClusterIP Service per broker ID — each resolving to a stable in-cluster DNS name — and Gateway uses SNI to route traffic to the correct broker.

`gateway.kafka.brokerIds` is required when `routing: sni`. It accepts a list of range specs:

| Format    | Example          | Expands to          |
|-----------|------------------|---------------------|
| Single ID | `"2"`            | 2                   |
| List      | `"0,1,2"`        | 0, 1, 2             |
| Range     | `"0-2"`          | 0, 1, 2             |
| Mixed     | `"0-2,10,12-13"` | 0, 1, 2, 10, 12, 13 |

> [!NOTE]
> Broker IDs do not need to start at 0 or be contiguous. Use whatever IDs match your Kafka cluster (e.g. `"100,104,110"`).

The chart auto-generates the advertised and bootstrap host patterns from the release name and namespace.

```yaml
gateway:
  preview:
    listeners: true
  securityMode: "GATEWAY_MANAGED"
  kafka:
    brokerIds:
      - "0-2"
  listeners:
    internal:
      securityProtocol: PLAINTEXT
      routing: sni
      ports:
        - "9092"
  env:
    KAFKA_BOOTSTRAP_SERVERS: kafka.default.svc.cluster.local:9092
```

This creates three ClusterIP Services:

* `<release>-gateway-broker-0.<namespace>.svc.<clusterDomain>`
* `<release>-gateway-broker-1.<namespace>.svc.<clusterDomain>`
* `<release>-gateway-broker-2.<namespace>.svc.<clusterDomain>`

And sets the bootstrap address to the internal service:

* `<release>-gateway-internal.<namespace>.svc.<clusterDomain>`

No additional DNS configuration is required — standard CoreDNS resolves all names automatically.

#### cert-manager TLS (automated certificate management)

When [cert-manager](https://cert-manager.io/) is installed in your cluster, you can let it provision and renew the Gateway TLS certificate automatically instead of managing a JKS secret by hand.

**Prerequisites:**

* cert-manager ≥ 0.15 installed in your cluster
* An `Issuer` or `ClusterIssuer` configured (self-signed, Let's Encrypt, Vault, etc.)
* `gateway.preview.listeners: true`

The chart auto-derives certificate SANs from the listener configuration — no manual DNS name list is needed for most setups.

> [!NOTE]
> Set `tls.certManager.truststore.enabled: false` when the upstream Kafka broker uses PLAINTEXT. Enabling it forces the gateway to open an SSL connection upstream, which will fail if Kafka is not TLS-enabled.

##### Internal SNI routing with cert-manager

The chart generates per-broker ClusterIP Services and includes their FQDNs as certificate SANs automatically.

```yaml
gateway:
  preview:
    listeners: true
  securityMode: "GATEWAY_MANAGED"
  kafka:
    brokerIds:
      - "0-2"
  listeners:
    internal:
      securityProtocol: SSL
      routing: sni
      ports:
        - "9092"
  env:
    KAFKA_BOOTSTRAP_SERVERS: kafka.default.svc.cluster.local:9092

tls:
  certManager:
    enabled: true
    issuerRef:
      name: letsencrypt-prod          # name of your Issuer or ClusterIssuer
      kind: ClusterIssuer
    truststore:
      enabled: false                  # set true only when upstream Kafka uses TLS or mTLS clients
```

cert-manager creates a secret named `<release>-tls` containing the JKS keystore.
The Gateway reloads the SSL context every `tls.certManager.sslContextRefreshMinutes` minutes (default 5), so certificate renewals are picked up automatically without a pod restart.

##### Internal port routing with cert-manager and secured admin API

Port-based routing assigns one port per broker; no per-broker Service is required. Optionally, the admin API can be served over HTTPS using the same certificate.

```yaml
gateway:
  preview:
    listeners: true
  securityMode: "GATEWAY_MANAGED"
  listeners:
    internal:
      securityProtocol: SSL
      routing: port
      ports:
        - "9092-9098"
  env:
    KAFKA_BOOTSTRAP_SERVERS: kafka.default.svc.cluster.local:9092

tls:
  certManager:
    enabled: true
    issuerRef:
      name: my-cluster-issuer
      kind: ClusterIssuer
    truststore:
      enabled: true                   # Mount cert-manager CA truststore
    httpsAdminApi:
      enabled: true                   # serve the admin API over HTTPS
```

##### Internal + external SNI routing with cert-manager

Both listeners can use cert-manager TLS. The chart adds the external advertised and bootstrap hostnames as SANs automatically. Use `tls.certManager.extraDnsNames` for any additional SANs.

```yaml
gateway:
  preview:
    listeners: true
  securityMode: "GATEWAY_MANAGED"
  kafka:
    brokerIds:
      - "0-2"
  listeners:
    internal:
      securityProtocol: SASL_SSL
      routing: sni
      ports:
        - "9092"
    external:
      securityProtocol: SASL_SSL
      routing: sni
      ports:
        - "19092"
      advertisedHost: "kafka.example.com"
      advertisedHostPattern: "broker-{{nodeId}}.kafka.example.com"
      bootstrapHostPattern: "bootstrap.kafka.example.com"
  env:
    KAFKA_BOOTSTRAP_SERVERS: kafka.default.svc.cluster.local:9092

tls:
  certManager:
    enabled: true
    issuerRef:
      name: letsencrypt-prod
      kind: ClusterIssuer
    duration: "2160h"                 # certificate validity (default 90 days)
    renewBefore: "360h"               # renew 15 days before expiry
    sslContextRefreshMinutes: 5       # how often Gateway polls the keystore for updates
    truststore:
      enabled: false
    httpsAdminApi:
      enabled: true
    extraDnsNames:
      - "extra.kafka.example.com"     # any additional SANs not auto-derived

service:
  external:
    enable: true
    type: LoadBalancer
    annotations:
      # if external-dns is available in cluster to automate DNS records creation
      external-dns.alpha.kubernetes.io/hostname: "kafka.example.com"
```

The chart automatically adds these SANs to the certificate:

* Per-broker services: `<release>-gateway-broker-<N>.<namespace>.svc.cluster.local` (internal SNI)
* Internal service FQDN: `<release>-gateway-internal.<namespace>.svc.cluster.local`
* External bootstrap: value of `bootstrapHostPattern` (wildcard-expanded for `{{nodeId}}` patterns)
* External per-broker wildcard from `advertisedHostPattern`

##### Using a custom Issuer namespace or group

For namespace-scoped Issuers or CRD groups other than `cert-manager.io`:

```yaml
tls:
  certManager:
    enabled: true
    issuerRef:
      name: my-issuer
      kind: Issuer                    # namespace-scoped
      group: cert-manager.io          # optional; defaults to cert-manager.io
```

##### Providing a custom password secret

By default the chart generates a random keystore password and stores it in a Secret. To use your own:

```yaml
tls:
  keystore:
    passwordSecretRef:
      name: my-tls-password-secret    # must exist before helm install
      key: password
  certManager:
    enabled: true
    issuerRef:
      name: my-issuer
      kind: ClusterIssuer
```

#### LoadBalancer chicken-and-egg problem

When using `service.external.enable: true`, you must set `gateway.listeners.external.advertisedHost` to the hostname clients will use. If your cloud provider assigns the LoadBalancer IP dynamically, you face a bootstrapping problem — the IP is unknown until after the Service is created.

Common approaches:

1. **Static IP reservation**: Reserve a static IP from your cloud provider and reference it in `service.external.ip` before deploying.

2. **Two-phase deploy**:
   1. Deploy with `service.external.enable: false` first to get the chart installed.
   2. Enable the external service: `kubectl patch ...` or `helm upgrade`.
   3. Retrieve the assigned IP: `kubectl get svc <release>-gateway-external -o jsonpath='{.status.loadBalancer.ingress[0].ip}'`
   4. Update `advertisedHost` and redeploy.

3. **DNS-based hostname**: Use a stable DNS name that you control, then update its A record once the IP is assigned.

#### Automating DNS with external-dns

[external-dns](https://github.com/kubernetes-sigs/external-dns) can automatically create DNS records for LoadBalancer services. It requires installing the external-dns controller in your cluster and configuring it for your DNS provider.

Once external-dns is running, annotate the external service so it creates the required records:

```yaml
service:
  external:
    enable: true
    type: LoadBalancer
    annotations:
      external-dns.alpha.kubernetes.io/hostname: "kafka.example.com"
```

For SNI listeners you also need wildcard records. Wildcard support varies by DNS provider — check the [external-dns documentation](https://github.com/kubernetes-sigs/external-dns) for your specific provider.

#### Migrating from single listener env var configuration

If you previously set `GATEWAY_LISTENER_*` environment variables directly via `gateway.env`, you can migrate to the chart-managed multi-listeners mode:

| Single listener `gateway.env` key | Multi-listeners mode equivalent |
|-----------------------------------|---------------------------------|
| `GATEWAY_SECURITY_MODE` | `gateway.securityMode` |
| `GATEWAY_ACL_ENABLED` | `gateway.aclEnabled` |
| `GATEWAY_LISTENER_NAMES` | derived from `service.external.enable` |
| `GATEWAY_LISTENER_INTERNAL_*` | `gateway.listeners.internal.*` |
| `GATEWAY_LISTENER_EXTERNAL_*` | `gateway.listeners.external.*` |

The chart emits a warning in `helm install` output if `GATEWAY_LISTENER_*` keys are found in `gateway.env` while `gateway.preview.listeners` is false — both cannot be mixed safely.

#### Migrating from single listener portRange to multi-listeners

`helm install` / `helm upgrade` output includes a generated starting-point config snippet derived from your current `gateway.portRange` and `gateway.env` values. Use it as a baseline and adjust as needed.

**Step 1 — Identify your current single listener configuration:**

```yaml
# Typical single listener values.yaml
gateway:
  portRange:
    start: 9092
    count: 4
  env:
    KAFKA_BOOTSTRAP_SERVERS: "kafka:9092"
    GATEWAY_SECURITY_PROTOCOL: "SASL_SSL"
    GATEWAY_ROUTING_MECHANISM: "host"     # "host" = SNI routing in the new API
    GATEWAY_ADVERTISED_HOST: "kafka.example.com"
    GATEWAY_SSL_KEY_STORE_PATH: "/etc/gateway/tls/keystore.jks"
    GATEWAY_SSL_KEY_STORE_PASSWORD: "changeit"
tls:
  enable: true
  secretRef: my-jks-secret
service:
  external:
    enable: true
    type: LoadBalancer
```

**Step 2 — Enable multi-listeners mode:**

Set `gateway.preview.listeners: true` and translate your single listener config into the listener objects. Keep all existing `gateway.env` vars in place during the initial migration — Gateway ignores single listener port vars in explicit multi-listeners mode, but removing them is a separate clean-up step.

```yaml
gateway:
  preview:
    listeners: true
  securityMode: "GATEWAY_MANAGED"
  kafka:
    brokerIds:
      - "0-2"                             # match your Kafka broker IDs
  listeners:
    internal:
      securityProtocol: SASL_SSL
      routing: sni
      ports:
        - "19092"
    external:
      securityProtocol: SASL_SSL
      routing: sni
      ports:
        - "9092"
      advertisedHost: "kafka.example.com"
      advertisedHostPattern: "broker-{{nodeId}}.kafka.example.com"
  env:
    KAFKA_BOOTSTRAP_SERVERS: "kafka:9092"
    # Keep during migration, remove in Step 3:
    # GATEWAY_SECURITY_PROTOCOL, GATEWAY_ROUTING_MECHANISM,
    # GATEWAY_ADVERTISED_HOST, GATEWAY_SSL_KEY_STORE_PATH, GATEWAY_SSL_KEY_STORE_PASSWORD

tls:
  enable: true
  secretRef: my-jks-secret

service:
  external:
    enable: true
    type: LoadBalancer
```

> [!NOTE]
> In multi-listeners mode, the internal and external listeners run inside the same Gateway pod, so they must bind to disjoint local port ranges to avoid conflicts. The single listener `gateway.portRange` exposed a single range shared by both internal and external services; when migrating, split it into two non-overlapping ranges (e.g. `19092-19095` for internal, `9092` for external).

**Single listener → multi-listeners field mapping:**

| Single listener `gateway.env` key | Multi-listeners equivalent |
| --- | --- |
| `GATEWAY_SECURITY_PROTOCOL` | `gateway.listeners.*.securityProtocol` |
| `GATEWAY_ROUTING_MECHANISM: "host"` | `gateway.listeners.*.routing: sni` |
| `GATEWAY_ROUTING_MECHANISM: "port"` | `gateway.listeners.*.routing: port` |
| `GATEWAY_ADVERTISED_HOST` | `gateway.listeners.external.advertisedHost` |
| `GATEWAY_PORT_START` / `gateway.portRange.start` | `gateway.listeners.*.ports` |
| `GATEWAY_PORT_COUNT` / `gateway.portRange.count` | `gateway.listeners.*.ports` (range length) |
| `GATEWAY_SECURITY_MODE` | `gateway.securityMode` |
| `GATEWAY_ACL_ENABLED` | `gateway.aclEnabled` |

**Step 3 — Clean up single listener env vars:**

After confirming the new multi-listeners config works, remove the single listener keys from `gateway.env` and remove `gateway.portRange`:

```yaml
# Keys to remove from gateway.env:
# GATEWAY_SECURITY_PROTOCOL, GATEWAY_ROUTING_MECHANISM,
# GATEWAY_ADVERTISED_HOST, GATEWAY_ADVERTISED_HOST_PREFIX, GATEWAY_SNI_HOST_SEPARATOR,
# GATEWAY_SSL_KEY_STORE_PATH, GATEWAY_SSL_KEY_STORE_PASSWORD
```
