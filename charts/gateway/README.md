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
| `gateway.image.tag`        | Image tag                                                | `3.10.0`                      |
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
| `gateway.interceptors`                       | Json configuration for interceptors to be loaded at startup by Gateway                                                                                                                                                                 | `[]`                                                                                                                                                                                                                                                                                                                        |
| `gateway.portRange.start`                    | Start port of the gateway port range                                                                                                                                                                                                   | `9092`                                                                                                                                                                                                                                                                                                                      |
| `gateway.portRange.count`                    | Max number of broker to expose                                                                                                                                                                                                         | `7`                                                                                                                                                                                                                                                                                                                         |
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
| `gateway.resources.limits.cpu`               | CPU limit for the platform container                                                                                                                                                                                                   | `2000m`                                                                                                                                                                                                                                                                                                                     |
| `gateway.resources.limits.memory`            | Memory limit for the container                                                                                                                                                                                                         | `4Gi`                                                                                                                                                                                                                                                                                                                       |
| `gateway.resources.requests.cpu`             | CPU resource requests                                                                                                                                                                                                                  | `500m`                                                                                                                                                                                                                                                                                                                      |
| `gateway.resources.requests.memory`          | Memory resource requests                                                                                                                                                                                                               | `500Mi`                                                                                                                                                                                                                                                                                                                     |
| `gateway.podLabels`                          | Specific labels to be added to Gateway pod by deployment                                                                                                                                                                               | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.podAnnotations`                     | Gateway pod annotations                                                                                                                                                                                                                | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.securityContext`                    | Conduktor Gateway container Security Context                                                                                                                                                                                           | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.volumes`                            | Define user specific volumes for Gateway deployment                                                                                                                                                                                    | `[]`                                                                                                                                                                                                                                                                                                                        |
| `gateway.volumeMounts`                       | Define user specific volumeMounts for Gateway container in deployment                                                                                                                                                                  | `[]`                                                                                                                                                                                                                                                                                                                        |
| `gateway.sidecars`                           | Add additional sidecar containers to run into the Conduktor Gateway pod(s)                                                                                                                                                             | `[]`                                                                                                                                                                                                                                                                                                                        |
| `gateway.initContainers`                     | Add additional init containers to the Conduktor Gateway pod(s). ref: https://kubernetes.io/docs/concepts/workloads/pods/init-containers/                                                                                               | `[]`                                                                                                                                                                                                                                                                                                                        |
| `gateway.terminationGracePeriodSeconds`      | Duration in seconds the pod needs to terminate gracefully.                                                                                                                                                                             | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.priorityClassName`                  | Define Gateway pods' priority based on an existing ClassName                                                                                                                                                                           | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.customStartupProbe`                 | Custom startup probe configuration                                                                                                                                                                                                     | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.startupProbe.enabled`               | Enable startupProbe on Conduktor Gaterway containers                                                                                                                                                                                   | `true`                                                                                                                                                                                                                                                                                                                      |
| `gateway.startupProbe.initialDelaySeconds`   | Initial delay seconds for startupProbe                                                                                                                                                                                                 | `10`                                                                                                                                                                                                                                                                                                                        |
| `gateway.startupProbe.periodSeconds`         | Period seconds for startupProbe                                                                                                                                                                                                        | `10`                                                                                                                                                                                                                                                                                                                        |
| `gateway.startupProbe.timeoutSeconds`        | Timeout seconds for startupProbe                                                                                                                                                                                                       | `1`                                                                                                                                                                                                                                                                                                                         |
| `gateway.startupProbe.failureThreshold`      | Failure threshold for startupProbe                                                                                                                                                                                                     | `5`                                                                                                                                                                                                                                                                                                                         |
| `gateway.startupProbe.successThreshold`      | Success threshold for startupProbe                                                                                                                                                                                                     | `1`                                                                                                                                                                                                                                                                                                                         |
| `gateway.customLivenessProbe`                | Custom liveness probe configuration                                                                                                                                                                                                    | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.livenessProbe.enabled`              | Enable livenessProbe on Conduktor Gaterway containers                                                                                                                                                                                  | `true`                                                                                                                                                                                                                                                                                                                      |
| `gateway.livenessProbe.initialDelaySeconds`  | Initial delay seconds for livenessProbe                                                                                                                                                                                                | `0`                                                                                                                                                                                                                                                                                                                         |
| `gateway.livenessProbe.periodSeconds`        | Period seconds for livenessProbe                                                                                                                                                                                                       | `5`                                                                                                                                                                                                                                                                                                                         |
| `gateway.livenessProbe.timeoutSeconds`       | Timeout seconds for livenessProbe                                                                                                                                                                                                      | `1`                                                                                                                                                                                                                                                                                                                         |
| `gateway.livenessProbe.failureThreshold`     | Failure threshold for livenessProbe                                                                                                                                                                                                    | `3`                                                                                                                                                                                                                                                                                                                         |
| `gateway.livenessProbe.successThreshold`     | Success threshold for livenessProbe                                                                                                                                                                                                    | `1`                                                                                                                                                                                                                                                                                                                         |
| `gateway.customReadinessProbe`               | Custom readiness probe configuration                                                                                                                                                                                                   | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.readinessProbe.enabled`             | Enable readinessProbe on Conduktor Gaterway containers                                                                                                                                                                                 | `true`                                                                                                                                                                                                                                                                                                                      |
| `gateway.readinessProbe.initialDelaySeconds` | Initial delay seconds for readinessProbe                                                                                                                                                                                               | `0`                                                                                                                                                                                                                                                                                                                         |
| `gateway.readinessProbe.periodSeconds`       | Period seconds for readinessProbe                                                                                                                                                                                                      | `5`                                                                                                                                                                                                                                                                                                                         |
| `gateway.readinessProbe.timeoutSeconds`      | Timeout seconds for readinessProbe                                                                                                                                                                                                     | `1`                                                                                                                                                                                                                                                                                                                         |
| `gateway.readinessProbe.failureThreshold`    | Failure threshold for readinessProbe                                                                                                                                                                                                   | `3`                                                                                                                                                                                                                                                                                                                         |
| `gateway.readinessProbe.successThreshold`    | Success threshold for readinessProbe                                                                                                                                                                                                   | `1`                                                                                                                                                                                                                                                                                                                         |

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
| `service.external.labels`      | Labels to be added to Gateway internal service      | `{}`        |
| `service.external.admin`       | Enable admin exposition on external service         | `false`     |
| `service.external.jmx`         | Enable jmx exposition on external service           | `false`     |

### Conduktor-gateway internal service configurations

This section specify internal service configuration

| Name                           | Description                                    | Value |
| ------------------------------ | ---------------------------------------------- | ----- |
| `service.internal.annotations` |                                                | `{}`  |
| `service.internal.labels`      | Labels to be added to Gateway internal service | `{}`  |

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

| Name                                          | Description                                                      | Value  |
| --------------------------------------------- | ---------------------------------------------------------------- | ------ |
| `serviceAccount.create`                       | Specifies whether a ServiceAccount should be created             | `true` |
| `serviceAccount.name`                         | The name of the ServiceAccount to use.                           | `""`   |
| `serviceAccount.annotations`                  | Additional Service Account annotations (evaluated as a template) | `{}`   |
| `serviceAccount.automountServiceAccountToken` | Automount service account token for the server service account   | `true` |
| `nodeSelector`                                | Container node selector                                          | `{}`   |
| `tolerations`                                 | Container tolerations                                            | `[]`   |
| `affinity`                                    | Container affinity                                               | `{}`   |
| `podSecurityContext`                          | Conduktor Gateway Pod Security Context                           | `{}`   |


## Example

* [How to provide secrets](#how-to-provide-secrets)
  * [Provide you own secret with `gateway.secretRef`](#provide-you-own-secret-with-gatewaysecretref)
  * [Using `gateway.extraSecretEnvVars`](#using-gatewayextrasecretenvvars)
  * [Using values and generated secrets](#using-values-and-generated-secrets)
  * [Pulling from private registry using `global.imagePullSecrets`](#pulling-from-private-registry-using-globalimagepullsecrets)
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
  ingress.annotations:
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
      readonly: true
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