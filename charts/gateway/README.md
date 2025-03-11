## Conduktor Gateway chart

A Kafka-protocol aware proxy.

See our [compatibility matrix](https://docs.conduktor.io/gateway/get-started/kubernetes/#helm-chart-compatibility)

## Installation

```sh
helm repo add conduktor https://helm.conduktor.io
helm repo update
helm install my-gateway conduktor/conduktor-gateway
```

## Parameters

### Global parameters

Global Docker image parameters
Please, note that this will override the image parameters, including dependencies, configured to use the global value
Current available global Docker image parameters: imageRegistry, imagePullSecrets and storageClass

| Name                      | Description                              | Value |
| ------------------------- | ---------------------------------------- | ----- |
| `global.imagePullSecrets` | Docker login secrets name for image pull | `[]`  |
| `global.env`              | The environment name                     | `""`  |

### Common parameters

| Name                | Description                                     | Value           |
| ------------------- | ----------------------------------------------- | --------------- |
| `nameOverride`      | String to partially override common.names.name  | `""`            |
| `fullnameOverride`  | String to fully override common.names.fullname  | `""`            |
| `namespaceOverride` | String to fully override common.names.namespace | `""`            |
| `commonLabels`      | Labels to add to all deployed objects           | `{}`            |
| `commonAnnotations` | Annotations to add to all deployed objects      | `{}`            |
| `clusterDomain`     | Kubernetes cluster domain name                  | `cluster.local` |

### Gateway image configuration

This section defines the image to be used.

| Name                       | Description                                              | Value                         |
| -------------------------- | -------------------------------------------------------- | ----------------------------- |
| `gateway.image.registry`   | Docker registry to use                                   | `docker.io`                   |
| `gateway.image.repository` | Image in repository format (conduktor/conduktor-gateway) | `conduktor/conduktor-gateway` |
| `gateway.image.tag`        | Image tag                                                | `3.6.1`                       |
| `gateway.image.pullPolicy` | Kubernetes image pull policy                             | `IfNotPresent`                |

### Gateway configurations

This section contains configuration of the Conduktor Gateway.

| Name                                         | Description                                                                                                                                                                       | Value                                                                                                                                                                                                                                                                                                                       |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gateway.replicas`                           | number of gateway instances to be deployed                                                                                                                                        | `2`                                                                                                                                                                                                                                                                                                                         |
| `gateway.secretRef`                          | Secret name to load sensitive env var from                                                                                                                                        | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.extraSecretEnvVars`                 | Array with extra secret environment variables                                                                                                                                     | `[]`                                                                                                                                                                                                                                                                                                                        |
| `gateway.secretSha256sum`                    | Optional sha256sum of the referenced secret. This could be set to have a automactic restart of gateway deployment if secret change                                                | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.env`                                | Environment variables for Gateway deployment                                                                                                                                      | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.licenseKey`                         | License key to activate Conduktor Gateway not used if `gateway.secretRef` is set                                                                                                  | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.interceptors`                       | Json configuration for interceptors to be loaded at startup by Gateway                                                                                                            | `[]`                                                                                                                                                                                                                                                                                                                        |
| `gateway.portRange.start`                    | Start port of the gateway port range                                                                                                                                              | `9092`                                                                                                                                                                                                                                                                                                                      |
| `gateway.portRange.count`                    | Max number of broker to expose                                                                                                                                                    | `7`                                                                                                                                                                                                                                                                                                                         |
| `gateway.admin.port`                         | Admin HTTP server port                                                                                                                                                            | `8888`                                                                                                                                                                                                                                                                                                                      |
| `gateway.admin.users[0].username`            | API Admin username. (not used if `gateway.secretRef` is set)                                                                                                                      | `admin`                                                                                                                                                                                                                                                                                                                     |
| `gateway.admin.users[0].password`            | API Admin password. If empty, a random password will be generated (not used if `gateway.secretRef` is set)                                                                        | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.admin.users[0].admin`               | API user admin role flag. (not used if `gateway.secretRef` is set)                                                                                                                | `true`                                                                                                                                                                                                                                                                                                                      |
| `gateway.admin.mainAdminSecretKeys.username` | Secret key used to store the username of the main admin user from `gateway.admin.users` (first with admin role)                                                                   | `GATEWAY_ADMIN_USERNAME`                                                                                                                                                                                                                                                                                                    |
| `gateway.admin.mainAdminSecretKeys.password` | Secret key used to store the password of the main admin user from `gateway.admin.users` (first with admin role)                                                                   | `GATEWAY_ADMIN_PASSWORD`                                                                                                                                                                                                                                                                                                    |
| `gateway.admin.securedMetrics`               | Enable secured metrics using api users credentials. If `gateway.secretRef` is set, this can't be used by `metrics.prometheus` to automatically configure basic auth on scrapping. | `true`                                                                                                                                                                                                                                                                                                                      |
| `gateway.jmx.enable`                         | Enable JMX JVM options                                                                                                                                                            | `false`                                                                                                                                                                                                                                                                                                                     |
| `gateway.jmx.port`                           | JMX port to expose by default JVM args                                                                                                                                            | `9999`                                                                                                                                                                                                                                                                                                                      |
| `gateway.jmx.jvmArgs`                        | Arguments to pass to the gateway container JVM                                                                                                                                    | `-Dcom.sun.management.jmxremote.port={{ .Values.gateway.jmx.port }} -Dcom.sun.management.jmxremote.rmi.port={{ .Values.gateway.jmx.port }} -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.local.only=false -Dcom.sun.management.jmxremote.ssl=false -Djava.rmi.server.hostname=127.0.0.1` |
| `gateway.startupProbeDelay`                  | Optional delay in second before startup probe should be running (default 10)                                                                                                      | `""`                                                                                                                                                                                                                                                                                                                        |
| `gateway.podLabels`                          | Specific labels to be added to Gateway pod by deployment                                                                                                                          | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.podAnnotations`                     | Gateway pod annotations                                                                                                                                                           | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.securityContext`                    | Container security context                                                                                                                                                        | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.volumes`                            | Define user specific volumes for Gateway deployment                                                                                                                               | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.volumeMounts`                       | Define user specific volumeMounts for Gateway container in deployment                                                                                                             | `{}`                                                                                                                                                                                                                                                                                                                        |
| `gateway.priorityClassName`                  | Define Gateway pods' priority based on an existing ClassName                                                                                                                      | `""`                                                                                                                                                                                                                                                                                                                        |

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

| Name                                     | Description                                                                                                                                                                        | Value                        |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| `metrics.alerts.enable`                  | Enable Prometheus alerts if Prometheus alerts rules are supported on cluster                                                                                                       | `false`                      |
| `metrics.prometheus.enable`              | Enable ServiceMonitor Prometheus operator configuration for metrics scrapping                                                                                                      | `false`                      |
| `metrics.prometheus.annotations`         | Additional custom annotations for the ServiceMonitor                                                                                                                               | `{}`                         |
| `metrics.prometheus.labels`              | Extra labels for the ServiceMonitor                                                                                                                                                | `{}`                         |
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

### Dependencies

Enable and configure chart dependencies if not available in your deployment.

| Name            | Description                                                                   | Value   |
| --------------- | ----------------------------------------------------------------------------- | ------- |
| `kafka.enabled` | Deploy a kafka along side gateway (This should only used for testing purpose) | `false` |


## Example

The following `values.yaml` file can be used to set up Gateway to proxy traffic to a Confluent Cloud cluster:

```yaml
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