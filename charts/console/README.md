<a name="readme-top" id="readme-top"></a>

# Conduktor Console

> If you have any questions you can [submit feedback](https://support.conduktor.io/hc/en-gb/requests/new?ticket_form_id=17438365654417) or contact [support](https://www.conduktor.io/contact/support/).

See our [compatibility matrix](https://docs.conduktor.io/platform/get-started/installation/get-started/kubernetes/#helm-chart-compatibility)

## TL;DR

```console
$ helm repo add conduktor https://helm.conduktor.io
$ helm install my-platform conduktor/console \
    --create-namespace -n conduktor \
    --set config.organization.name="my-org" \
    --set config.admin.email="admin@conduktor.io" \
    --set config.admin.password="Admin123!" \
    --set config.database.url="jdbc:postgresql://postgres:password@postgresql:5432/postgres" \
    --set config.license="${LICENSE}"
```

## Introduction

Helm Chart to deploy Conduktor Console on Kubernetes.

[Snippets](#snippets) are available in this README to help you get started.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+

* [Parameters](#parameters)
  * [Global parameters](#global-parameters)
  * [Common parameters](#common-parameters)
  * [Platform product Parameters](#platform-product-parameters)
  * [Platform Monitoring product Parameters](#platform-monitoring-product-parameters)
  * [Platform Deployment Parameters](#platform-deployment-parameters)
  * [Platform Metrics activation](#platform-metrics-activation)
  * [Traffic Exposure Parameters](#traffic-exposure-parameters)
  * [Other Parameters](#other-parameters)
  * [Platform Cortex Parameters](#platform-cortex-parameters)
* [Snippets](#snippets)
* [Troubleshooting](#troubleshooting)

## Parameters

### Global parameters

Global Docker image parameters
Please, note that this will override the image parameters, including dependencies, configured to use the global value
Current available global Docker image parameters: imageRegistry, imagePullSecrets and storageClass

| Name                      | Description                                     | Value |
| ------------------------- | ----------------------------------------------- | ----- |
| `global.imageRegistry`    | Global Docker image registry                    | `""`  |
| `global.imagePullSecrets` | Global Docker registry secret names as an array | `[]`  |
| `global.storageClass`     | Global StorageClass for Persistent Volume(s)    | `""`  |

### Common parameters

| Name                     | Description                                                                             | Value           |
| ------------------------ | --------------------------------------------------------------------------------------- | --------------- |
| `nameOverride`           | String to partially override common.names.name                                          | `""`            |
| `fullnameOverride`       | String to fully override common.names.fullname                                          | `""`            |
| `namespaceOverride`      | String to fully override common.names.namespace                                         | `""`            |
| `commonLabels`           | Labels to add to all deployed objects                                                   | `{}`            |
| `commonAnnotations`      | Annotations to add to all deployed objects                                              | `{}`            |
| `clusterDomain`          | Kubernetes cluster domain name                                                          | `cluster.local` |
| `extraDeploy`            | Array of extra objects to deploy with the release                                       | `[]`            |
| `diagnosticMode.enabled` | Enable diagnostic mode (all probes will be disabled and the command will be overridden) | `false`         |
| `diagnosticMode.command` | Command to override all containers in the deployment                                    | `["sleep"]`     |
| `diagnosticMode.args`    | Args to override all containers in the deployment                                       | `["infinity"]`  |

### Platform product Parameters

You can paste here your Conduktor Console Configuration.

Refer to our [documentation](https://docs.conduktor.io/platform/configuration/env-variables/) for the full list of product configuration properties.

A list of Kafka clusters can be configured by adding them under the `config.clusters` key. See [Install with a Kafka cluster](#install-with-a-kafka-cluster) below. Alternatively, clusters can be added in the Console UI.

| Name                                   | Description                                                                                                                                     | Value       |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| `config.organization.name`             | Your Conduktor Console Organization. Default is `Conduktor` if not set.                                                                         | `Conduktor` |
| `config.admin.email`                   | Your Conduktor Console Admin email. If changed a new admin user will be created with this email and previous admin user will still be available | `""`        |
| `config.admin.password`                | Your Conduktor Console Admin password. If change current admin user password will be updated.                                                   | `""`        |
| `config.database.url`                  | Your Conduktor Console Database URL (postgresql or jdbc format)                                                                                 | `""`        |
| `config.database.hosts`                | List of Conduktor Console Database hosts (host and port)                                                                                        | `[]`        |
| `config.database.hosts[].host`         | Conduktor Console Database host                                                                                                                 |             |
| `config.database.hosts[].port`         | Conduktor Console Database port                                                                                                                 |             |
| `config.database.host`                 | **Deprecated** Conduktor Console Database host. Automatically fallback to `config.database.hosts[0].host` if set                                |             |
| `config.database.port`                 | **Deprecated** Conduktor Console Database port. Automatically fallback to `config.database.hosts[0].port` if set                                |             |
| `config.database.name`                 | Your Conduktor Console Database name                                                                                                            | `""`        |
| `config.database.username`             | Your Conduktor Console Database username                                                                                                        | `""`        |
| `config.database.password`             | Your Conduktor Console Database password                                                                                                        | `""`        |
| `config.license`                       | Conduktor Console Enterprise license, if none given, the product will run in free tier                                                          | `""`        |
| `config.existingLicenseSecret`         | Name of an existing secret containing the license                                                                                               | `""`        |
| `config.existingSecret`                | Name of an existing secret containing sensitive configuration                                                                                   | `""`        |
| `config.platform.external.url`         | Force the platform to redirect and use this URL (useful when behind a proxy to fix SSO issues)                                                  | `""`        |
| `config.platform.https.selfSigned`     | Enable HTTPS with a self-signed certificate (not recommended for production) based on 'config.platform.external.url' (required).                | `false`     |
| `config.platform.https.existingSecret` | Enable HTTPS with an existing secret containing the tls.crt and tls.key (required).                                                             | `""`        |

### Platform Monitoring product Parameters

You can paste here your Conduktor Console Cortex Configuration.

Refer to our [documentation](https://docs.conduktor.io/platform/configuration/cortex/) for the full list of product configuration properties.

| Name                                            | Description                                                                                | Value   |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------ | ------- |
| `monitoringConfig.existingSecret`               | The name of an existing Secret with your custom configuration for Conduktor Console Cortex | `""`    |
| `monitoringConfig.scraper.skipSSLCheck`         | Skip TLS verification when scraping Platform metrics                                       | `false` |
| `monitoringConfig.scraper.caFile`               | Skip TLS verification when scraping Platform metrics                                       | `""`    |
| `monitoringConfig.storage.s3`                   | S3 storage configuration                                                                   | `{}`    |
| `monitoringConfig.storage.s3.endpoint`          | S3 endpoint                                                                                |         |
| `monitoringConfig.storage.s3.region`            | S3 region                                                                                  |         |
| `monitoringConfig.storage.s3.bucket`            | S3 bucket name                                                                             |         |
| `monitoringConfig.storage.s3.insecure`          | S3 insecure                                                                                |         |
| `monitoringConfig.storage.s3.accessKeyId`       | S3 access key id                                                                           |         |
| `monitoringConfig.storage.s3.secretAccessKey`   | S3 secret access key                                                                       |         |
| `monitoringConfig.storage.gcs`                  | GCS storage configuration                                                                  | `{}`    |
| `monitoringConfig.storage.gcs.bucketName`       | GCS bucket name                                                                            |         |
| `monitoringConfig.storage.gcs.serviceAccount`   | GCS service account                                                                        |         |
| `monitoringConfig.storage.azure`                | Azure storage configuration                                                                | `{}`    |
| `monitoringConfig.storage.azure.accountName`    | Azure account name                                                                         |         |
| `monitoringConfig.storage.azure.accountKey`     | Azure account key                                                                          |         |
| `monitoringConfig.storage.azure.containerName`  | Azure container name                                                                       |         |
| `monitoringConfig.storage.azure.endpointSuffix` | Azure endpoint suffix                                                                      |         |
| `monitoringConfig.storage.swift`                | Swift storage configuration                                                                | `{}`    |
| `monitoringConfig.storage.swift.authUrl`        | Swift auth url                                                                             |         |
| `monitoringConfig.storage.swift.password`       | Swift password                                                                             |         |
| `monitoringConfig.storage.swift.containerName`  | Swift container name                                                                       |         |
| `monitoringConfig.storage.swift.userId`         | Swift user id                                                                              |         |
| `monitoringConfig.storage.swift.username`       | Swift username                                                                             |         |
| `monitoringConfig.storage.swift.userDomainName` | Swift user domain name                                                                     |         |
| `monitoringConfig.storage.swift.userDomainId`   | Swift user domain id                                                                       |         |
| `monitoringConfig.storage.swift.domainId`       | Swift domain id                                                                            |         |
| `monitoringConfig.storage.swift.domainName`     | Swift domain name                                                                          |         |
| `monitoringConfig.storage.swift.projectId`      | Swift project id                                                                           |         |
| `monitoringConfig.storage.swift.regionName`     | Swift region name                                                                          |         |

### Platform Deployment Parameters

| Name                                          | Description                                                                                                                                                  | Value                         |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------- |
| `platform.image.registry`                     | Conduktor Console image registry                                                                                                                             | `docker.io`                   |
| `platform.image.repository`                   | Conduktor Console image repository                                                                                                                           | `conduktor/conduktor-console` |
| `platform.image.tag`                          | Conduktor Console image tag (immutable tags are recommended)                                                                                                 | `1.43.1`                      |
| `platform.image.digest`                       | Conduktor Console image digest in the way sha256:aa.... Please note this parameter, if set, will override the tag image tag (immutable tags are recommended) | `""`                          |
| `platform.image.pullPolicy`                   | Conduktor Console image pull policy                                                                                                                          | `IfNotPresent`                |
| `platform.image.pullSecrets`                  | Conduktor Console image pull secrets                                                                                                                         | `[]`                          |
| `platform.image.debug`                        | Enable Conduktor Console image debug mode                                                                                                                    | `false`                       |
| `platform.replicaCount`                       | Number of Conduktor Console replicas to deploy                                                                                                               | `1`                           |
| `platform.containerPorts.http`                | Conduktor Console HTTP (or HTTPS if configured) container port                                                                                               | `8080`                        |
| `platform.livenessProbe.enabled`              | Enable livenessProbe on Conduktor Console containers                                                                                                         | `true`                        |
| `platform.livenessProbe.initialDelaySeconds`  | Initial delay seconds for livenessProbe                                                                                                                      | `60`                          |
| `platform.livenessProbe.periodSeconds`        | Period seconds for livenessProbe                                                                                                                             | `10`                          |
| `platform.livenessProbe.timeoutSeconds`       | Timeout seconds for livenessProbe                                                                                                                            | `5`                           |
| `platform.livenessProbe.failureThreshold`     | Failure threshold for livenessProbe                                                                                                                          | `3`                           |
| `platform.livenessProbe.successThreshold`     | Success threshold for livenessProbe                                                                                                                          | `1`                           |
| `platform.readinessProbe.enabled`             | Enable readinessProbe on Conduktor Console containers                                                                                                        | `true`                        |
| `platform.readinessProbe.initialDelaySeconds` | Initial delay seconds for readinessProbe                                                                                                                     | `60`                          |
| `platform.readinessProbe.periodSeconds`       | Period seconds for readinessProbe                                                                                                                            | `10`                          |
| `platform.readinessProbe.timeoutSeconds`      | Timeout seconds for readinessProbe                                                                                                                           | `5`                           |
| `platform.readinessProbe.failureThreshold`    | Failure threshold for readinessProbe                                                                                                                         | `3`                           |
| `platform.readinessProbe.successThreshold`    | Success threshold for readinessProbe                                                                                                                         | `1`                           |
| `platform.startupProbe.enabled`               | Enable startupProbe on Conduktor Console containers                                                                                                          | `true`                        |
| `platform.startupProbe.initialDelaySeconds`   | Initial delay seconds for startupProbe                                                                                                                       | `10`                          |
| `platform.startupProbe.periodSeconds`         | Period seconds for startupProbe                                                                                                                              | `10`                          |
| `platform.startupProbe.timeoutSeconds`        | Timeout seconds for startupProbe                                                                                                                             | `5`                           |
| `platform.startupProbe.failureThreshold`      | Failure threshold for startupProbe                                                                                                                           | `10`                          |
| `platform.startupProbe.successThreshold`      | Success threshold for startupProbe                                                                                                                           | `1`                           |
| `platform.customLivenessProbe`                | Custom livenessProbe that overrides the default one                                                                                                          | `{}`                          |
| `platform.customReadinessProbe`               | Custom readinessProbe that overrides the default one                                                                                                         | `{}`                          |
| `platform.customStartupProbe`                 | Custom startupProbe that overrides the default one                                                                                                           | `{}`                          |
| `platform.resources.limits.cpu`               | CPU limit for the platform container                                                                                                                         | `3000m`                       |
| `platform.resources.limits.memory`            | Memory limit for the container                                                                                                                               | `4Gi`                         |
| `platform.resources.requests.cpu`             | CPU resource requests                                                                                                                                        | `1000m`                       |
| `platform.resources.requests.memory`          | Memory resource requests                                                                                                                                     | `2Gi`                         |
| `platform.podSecurityContext`                 | Conduktor Console Pod Security Context                                                                                                                       | `{}`                          |
| `platform.containerSecurityContext`           | Conduktor Console containers' Security Context                                                                                                               | `{}`                          |
| `platform.existingConfigmap`                  | The name of an existing ConfigMap with your custom configuration for Conduktor Console                                                                       | `""`                          |
| `platform.command`                            | Override default container command (useful when using custom images)                                                                                         | `[]`                          |
| `platform.args`                               | Override default container args (useful when using custom images)                                                                                            | `[]`                          |
| `platform.hostAliases`                        | Conduktor Console pods host aliases                                                                                                                          | `[]`                          |
| `platform.podLabels`                          | Extra labels for Conduktor Console pods                                                                                                                      | `{}`                          |
| `platform.podAnnotations`                     | Annotations for Conduktor Console pods                                                                                                                       | `{}`                          |
| `platform.podAffinityPreset`                  | Pod affinity preset. Ignored if `platform.affinity` is set. Allowed values: `soft` or `hard`                                                                 | `""`                          |
| `platform.podAntiAffinityPreset`              | Pod anti-affinity preset. Ignored if `platform.affinity` is set. Allowed values: `soft` or `hard`                                                            | `soft`                        |
| `platform.nodeAffinityPreset.type`            | Node affinity preset type. Ignored if `platform.affinity` is set. Allowed values: `soft` or `hard`                                                           | `""`                          |
| `platform.nodeAffinityPreset.key`             | Node label key to match. Ignored if `platform.affinity` is set                                                                                               | `""`                          |
| `platform.nodeAffinityPreset.values`          | Node label values to match. Ignored if `platform.affinity` is set                                                                                            | `[]`                          |
| `platform.affinity`                           | Affinity for Conduktor Console pods assignment                                                                                                               | `{}`                          |
| `platform.nodeSelector`                       | Node labels for Conduktor Console pods assignment                                                                                                            | `{}`                          |
| `platform.tolerations`                        | Tolerations for Conduktor Console pods assignment                                                                                                            | `[]`                          |
| `platform.updateStrategy.type`                | Conduktor Console statefulset strategy type                                                                                                                  | `RollingUpdate`               |
| `platform.priorityClassName`                  | Conduktor Console pods' priorityClassName                                                                                                                    | `""`                          |
| `platform.topologySpreadConstraints`          | Topology Spread Constraints for pod assignment spread across your cluster among failure-domains. Evaluated as a template                                     | `[]`                          |
| `platform.schedulerName`                      | Name of the k8s scheduler (other than default) for Conduktor Console pods                                                                                    | `""`                          |
| `platform.terminationGracePeriodSeconds`      | Seconds Redmine pod needs to terminate gracefully                                                                                                            | `30`                          |
| `platform.lifecycleHooks`                     | for the Conduktor Console container(s) to automate configuration before or after startup                                                                     | `{}`                          |
| `platform.dataVolume`                         | Configure the data volume to store Conduktor Console data                                                                                                    | `{}`                          |
| `platform.tmpVolume`                          | Configure the /tmp volume which store various data related to running services                                                                               | `{}`                          |
| `platform.extraEnvVars`                       | Array with extra environment variables to add to Conduktor Console nodes                                                                                     | `[]`                          |
| `platform.extraEnvVarsCM`                     | Name of existing ConfigMap containing extra env vars for Conduktor Console nodes                                                                             | `""`                          |
| `platform.extraEnvVarsSecret`                 | Name of existing Secret containing extra env vars for Conduktor Console nodes                                                                                | `""`                          |
| `platform.extraVolumes`                       | Optionally specify extra list of additional volumes for the Conduktor Console pod(s).                                                                        | `[]`                          |
| `platform.extraVolumeMounts`                  | Optionally specify extra list of additional volumeMounts for the Conduktor Console container(s).                                                             | `[]`                          |
| `platform.sidecars`                           | Add additional sidecar containers to the Conduktor Console pod(s)                                                                                            | `[]`                          |
| `platform.initContainers`                     | Add additional init containers to the Conduktor Console pod(s)                                                                                               | `[]`                          |

### Platform Metrics activation

Console expose metrics that could be collected and presented if your environment have the necessary components (Prometheus and Grafana operators)

| Name                                                | Description                                                                                                                                                                 | Value                    |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| `platform.metrics.enabled`                          | Enable the export of Prometheus metrics                                                                                                                                     | `false`                  |
| `platform.metrics.serviceMonitor.enabled`           | if `true`, creates a Prometheus Operator ServiceMonitor (also requires `metrics.enabled` to be `true`)                                                                      | `false`                  |
| `platform.metrics.serviceMonitor.namespace`         | Namespace in which Prometheus is running                                                                                                                                    | `""`                     |
| `platform.metrics.serviceMonitor.annotations`       | Additional custom annotations for the ServiceMonitor                                                                                                                        | `{}`                     |
| `platform.metrics.serviceMonitor.labels`            | Extra labels for the ServiceMonitor                                                                                                                                         | `{}`                     |
| `platform.metrics.serviceMonitor.jobLabel`          | The name of the label on the target service to use as the job name in Prometheus                                                                                            | `app.kubernetes.io/name` |
| `platform.metrics.serviceMonitor.honorLabels`       | honorLabels chooses the metric's labels on collisions with target labels                                                                                                    | `false`                  |
| `platform.metrics.serviceMonitor.interval`          | Interval at which metrics should be scraped.                                                                                                                                | `""`                     |
| `platform.metrics.serviceMonitor.scheme`            | Protocol scheme to use for scraping (http or https). By default, automatically resolved based on container TLS configuration.                                               | `""`                     |
| `platform.metrics.serviceMonitor.tlsConfig`         | TLS configuration for the ServiceMonitor. By default, automatically resolved based on container TLS configuration using config.platform.https config and tls.crt in secret. | `{}`                     |
| `platform.metrics.serviceMonitor.scrapeTimeout`     | Timeout after which the scrape is ended                                                                                                                                     | `""`                     |
| `platform.metrics.serviceMonitor.metricRelabelings` | Specify additional relabeling of metrics                                                                                                                                    | `[]`                     |
| `platform.metrics.serviceMonitor.relabelings`       | Specify general relabeling                                                                                                                                                  | `[]`                     |
| `platform.metrics.serviceMonitor.selector`          | Prometheus instance selector labels                                                                                                                                         | `{}`                     |
| `platform.metrics.serviceMonitor.extraParams`       | Extra parameters for the ServiceMonitor                                                                                                                                     | `{}`                     |
| `platform.metrics.grafana.enabled`                  | Enable grafana dashboards to installation                                                                                                                                   | `false`                  |
| `platform.metrics.grafana.namespace`                | Namespace used to deploy Grafana dashboards by default use the same namespace as Conduktor Csonsole                                                                         | `""`                     |
| `platform.metrics.grafana.matchLabels`              | Label selector for Grafana instance                                                                                                                                         | `{}`                     |
| `platform.metrics.grafana.labels`                   | Additional custom labels for Grafana dashboard ConfigMap                                                                                                                    | `{}`                     |
| `platform.metrics.grafana.folder`                   | Grafana dashboard folder name                                                                                                                                               | `""`                     |
| `platform.metrics.grafana.datasources.prometheus`   | Prometheus datasource to use for metric dashboard                                                                                                                           | `prometheus`             |

### Traffic Exposure Parameters

| Name                               | Description                                                                                                                      | Value                    |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| `service.type`                     | Conduktor Console service type                                                                                                   | `ClusterIP`              |
| `service.ports.http`               | Conduktor Console service HTTP port                                                                                              | `80`                     |
| `service.nodePorts.http`           | Node port for HTTP                                                                                                               | `""`                     |
| `service.clusterIP`                | Conduktor Console service Cluster IP                                                                                             | `""`                     |
| `service.loadBalancerSourceRanges` | Conduktor Console service Load Balancer sources                                                                                  | `[]`                     |
| `service.externalTrafficPolicy`    | Conduktor Console service external traffic policy                                                                                | `Cluster`                |
| `service.labels`                   | Additional custom labels for Conduktor Console service                                                                           | `{}`                     |
| `service.annotations`              | Additional custom annotations for Conduktor Console service                                                                      | `{}`                     |
| `service.extraPorts`               | Extra ports to expose in Conduktor Console service (normally used with the `sidecars` value)                                     | `[]`                     |
| `service.sessionAffinity`          | Control where client requests go, to the same pod or round-robin                                                                 | `None`                   |
| `service.sessionAffinityConfig`    | Additional settings for the sessionAffinity                                                                                      | `{}`                     |
| `service.extraSpecs`               | Extra specs for the service to be added under `spec` key                                                                         | `{}`                     |
| `ingress.enabled`                  | Enable ingress record generation for Conduktor Console                                                                           | `false`                  |
| `ingress.pathType`                 | Ingress path type                                                                                                                | `ImplementationSpecific` |
| `ingress.apiVersion`               | Force Ingress API version (automatically detected if not set)                                                                    | `""`                     |
| `ingress.hostname`                 | Default host for the ingress record                                                                                              | `platform.local`         |
| `ingress.ingressClassName`         | IngressClass that will be used to implement the Ingress (Kubernetes 1.18+)                                                       | `""`                     |
| `ingress.path`                     | Default path for the ingress record                                                                                              | `/`                      |
| `ingress.annotations`              | Additional annotations for the Ingress resource. To enable certificate autogeneration, place here your cert-manager annotations. | `{}`                     |
| `ingress.tls`                      | Enable TLS configuration for the host defined at `ingress.hostname` parameter                                                    | `false`                  |
| `ingress.selfSigned`               | Create a TLS secret for this ingress record using self-signed certificates generated by Helm                                     | `false`                  |
| `ingress.extraHosts`               | An array with additional hostname(s) to be covered with the ingress record                                                       | `[]`                     |
| `ingress.extraPaths`               | An array with additional arbitrary paths that may need to be added to the ingress under the main host                            | `[]`                     |
| `ingress.extraTls`                 | TLS configuration for additional hostname(s) to be covered with this ingress record                                              | `[]`                     |
| `ingress.secrets`                  | Existing TLS secrets or custom TLS certificates/keys secrets to create and use                                                   | `[]`                     |
| `ingress.extraRules`               | Additional rules to be covered with this ingress record                                                                          | `[]`                     |

### Other Parameters

| Name                                          | Description                                                      | Value  |
| --------------------------------------------- | ---------------------------------------------------------------- | ------ |
| `serviceAccount.create`                       | Specifies whether a ServiceAccount should be created             | `true` |
| `serviceAccount.name`                         | The name of the ServiceAccount to use.                           | `""`   |
| `serviceAccount.annotations`                  | Additional Service Account annotations (evaluated as a template) | `{}`   |
| `serviceAccount.automountServiceAccountToken` | Automount service account token for the server service account   | `true` |

### Platform Cortex Parameters

| Name                                                | Description                                                                                                                                                         | Value                                |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `platformCortex.enabled`                            | Enable Conduktor Console Cortex                                                                                                                                     | `true`                               |
| `platformCortex.image.registry`                     | Conduktor Console Cortex image registry                                                                                                                             | `docker.io`                          |
| `platformCortex.image.repository`                   | Conduktor Console Cortex image repository                                                                                                                           | `conduktor/conduktor-console-cortex` |
| `platformCortex.image.tag`                          | Conduktor Console Cortex image tag (immutable tags are recommended)                                                                                                 | `1.43.1`                             |
| `platformCortex.image.digest`                       | Conduktor Console Cortex image digest in the way sha256:aa.... Please note this parameter, if set, will override the tag image tag (immutable tags are recommended) | `""`                                 |
| `platformCortex.image.pullPolicy`                   | Conduktor Console Cortex image pull policy                                                                                                                          | `IfNotPresent`                       |
| `platformCortex.image.pullSecrets`                  | Conduktor Console Cortex image pull secrets                                                                                                                         | `[]`                                 |
| `platformCortex.image.debug`                        | Enable Conduktor Console Cortex image debug mode                                                                                                                    | `false`                              |
| `platformCortex.replicaCount`                       | Number of Conduktor Console Cortex replicas to deploy                                                                                                               | `1`                                  |
| `platformCortex.containerPorts.cortex`              | Conduktor Console Cortex HTTP (or HTTPS if configured) container port                                                                                               | `9009`                               |
| `platformCortex.containerPorts.alertmanager`        | Conduktor Console AlertManager HTTP (or HTTPS if configured) container port                                                                                         | `9010`                               |
| `platformCortex.containerPorts.prometheus`          | Conduktor Console Prometheus HTTP (or HTTPS if configured) container port                                                                                           | `9090`                               |
| `platformCortex.livenessProbe.enabled`              | Enable livenessProbe on Conduktor Console Cortex containers                                                                                                         | `true`                               |
| `platformCortex.livenessProbe.initialDelaySeconds`  | Initial delay seconds for livenessProbe                                                                                                                             | `30`                                 |
| `platformCortex.livenessProbe.periodSeconds`        | Period seconds for livenessProbe                                                                                                                                    | `10`                                 |
| `platformCortex.livenessProbe.timeoutSeconds`       | Timeout seconds for livenessProbe                                                                                                                                   | `5`                                  |
| `platformCortex.livenessProbe.failureThreshold`     | Failure threshold for livenessProbe                                                                                                                                 | `3`                                  |
| `platformCortex.livenessProbe.successThreshold`     | Success threshold for livenessProbe                                                                                                                                 | `1`                                  |
| `platformCortex.readinessProbe.enabled`             | Enable readinessProbe on Conduktor Console Cortex containers                                                                                                        | `true`                               |
| `platformCortex.readinessProbe.initialDelaySeconds` | Initial delay seconds for readinessProbe                                                                                                                            | `30`                                 |
| `platformCortex.readinessProbe.periodSeconds`       | Period seconds for readinessProbe                                                                                                                                   | `10`                                 |
| `platformCortex.readinessProbe.timeoutSeconds`      | Timeout seconds for readinessProbe                                                                                                                                  | `5`                                  |
| `platformCortex.readinessProbe.failureThreshold`    | Failure threshold for readinessProbe                                                                                                                                | `3`                                  |
| `platformCortex.readinessProbe.successThreshold`    | Success threshold for readinessProbe                                                                                                                                | `1`                                  |
| `platformCortex.startupProbe.enabled`               | Enable startupProbe on Conduktor Console Cortex containers                                                                                                          | `false`                              |
| `platformCortex.startupProbe.initialDelaySeconds`   | Initial delay seconds for startupProbe                                                                                                                              | `10`                                 |
| `platformCortex.startupProbe.periodSeconds`         | Period seconds for startupProbe                                                                                                                                     | `10`                                 |
| `platformCortex.startupProbe.timeoutSeconds`        | Timeout seconds for startupProbe                                                                                                                                    | `5`                                  |
| `platformCortex.startupProbe.failureThreshold`      | Failure threshold for startupProbe                                                                                                                                  | `10`                                 |
| `platformCortex.startupProbe.successThreshold`      | Success threshold for startupProbe                                                                                                                                  | `1`                                  |
| `platformCortex.customLivenessProbe`                | Custom livenessProbe that overrides the default one                                                                                                                 | `{}`                                 |
| `platformCortex.customReadinessProbe`               | Custom readinessProbe that overrides the default one                                                                                                                | `{}`                                 |
| `platformCortex.customStartupProbe`                 | Custom startupProbe that overrides the default one                                                                                                                  | `{}`                                 |
| `platformCortex.resources.limits.cpu`               | CPU limit for the platform cortex container                                                                                                                         | `2000m`                              |
| `platformCortex.resources.limits.memory`            | Memory limit for the container                                                                                                                                      | `2Gi`                                |
| `platformCortex.resources.requests.cpu`             | CPU resource requests                                                                                                                                               | `500m`                               |
| `platformCortex.resources.requests.memory`          | Memory resource requests                                                                                                                                            | `500Mi`                              |
| `platformCortex.podSecurityContext`                 | Conduktor Console Cortex Pod Security Context                                                                                                                       | `{}`                                 |
| `platformCortex.containerSecurityContext`           | Conduktor Console Cortex containers' Security Context                                                                                                               | `{}`                                 |
| `platformCortex.existingConfigmap`                  | The name of an existing ConfigMap with your custom configuration for Conduktor Console Cortex                                                                       | `""`                                 |
| `platformCortex.command`                            | Override default container command (useful when using custom images)                                                                                                | `[]`                                 |
| `platformCortex.args`                               | Override default container args (useful when using custom images)                                                                                                   | `[]`                                 |
| `platformCortex.hostAliases`                        | Conduktor Console Cortex pods host aliases                                                                                                                          | `[]`                                 |
| `platformCortex.podLabels`                          | Extra labels for Conduktor Console Cortex pods                                                                                                                      | `{}`                                 |
| `platformCortex.podAnnotations`                     | Annotations for Conduktor Console Cortex pods                                                                                                                       | `{}`                                 |
| `platformCortex.podAffinityPreset`                  | Pod affinity preset. Ignored if `platform.affinity` is set. Allowed values: `soft` or `hard`                                                                        | `""`                                 |
| `platformCortex.podAntiAffinityPreset`              | Pod anti-affinity preset. Ignored if `platform.affinity` is set. Allowed values: `soft` or `hard`                                                                   | `soft`                               |
| `platformCortex.nodeAffinityPreset.type`            | Node affinity preset type. Ignored if `platform.affinity` is set. Allowed values: `soft` or `hard`                                                                  | `""`                                 |
| `platformCortex.nodeAffinityPreset.key`             | Node label key to match. Ignored if `platform.affinity` is set                                                                                                      | `""`                                 |
| `platformCortex.nodeAffinityPreset.values`          | Node label values to match. Ignored if `platform.affinity` is set                                                                                                   | `[]`                                 |
| `platformCortex.affinity`                           | Affinity for Conduktor Console cortex pods assignment                                                                                                               | `{}`                                 |
| `platformCortex.nodeSelector`                       | Node labels for Conduktor Console Cortex pods assignment                                                                                                            | `{}`                                 |
| `platformCortex.tolerations`                        | Tolerations for Conduktor Console Cortex pods assignment                                                                                                            | `[]`                                 |
| `platformCortex.updateStrategy.type`                | Conduktor Console Cortex statefulset strategy type                                                                                                                  | `RollingUpdate`                      |
| `platformCortex.priorityClassName`                  | Conduktor Console Cortex pods' priorityClassName                                                                                                                    | `""`                                 |
| `platformCortex.topologySpreadConstraints`          | Topology Spread Constraints for pod assignment spread across your cluster among failure-domains. Evaluated as a template                                            | `[]`                                 |
| `platformCortex.schedulerName`                      | Name of the k8s scheduler (other than default) for Conduktor Console Cortex pods                                                                                    | `""`                                 |
| `platformCortex.terminationGracePeriodSeconds`      | Seconds Redmine pod needs to terminate gracefully                                                                                                                   | `""`                                 |
| `platformCortex.lifecycleHooks`                     | for the Conduktor Console Cortex container(s) to automate configuration before or after startup                                                                     | `{}`                                 |
| `platformCortex.extraEnvVars`                       | Array with extra environment variables to add to Conduktor Console Cortex nodes                                                                                     | `[]`                                 |
| `platformCortex.extraEnvVarsCM`                     | Name of existing ConfigMap containing extra env vars for Conduktor Console Cortex nodes                                                                             | `""`                                 |
| `platformCortex.extraEnvVarsSecret`                 | Name of existing Secret containing extra env vars for Conduktor Console Cortex nodes                                                                                | `""`                                 |
| `platformCortex.dataVolume`                         | Configure the data volume to store Conduktor Console Cortex data                                                                                                    | `{}`                                 |
| `platformCortex.tmpVolume`                          | Configure the /tmp volume which store various data related to running services                                                                                      | `{}`                                 |
| `platformCortex.extraVolumes`                       | Optionally specify extra list of additional volumes for the Conduktor Console Cortex pod(s)                                                                         | `[]`                                 |
| `platformCortex.extraVolumeMounts`                  | Optionally specify extra list of additional volumeMounts for the Conduktor Console Cortex container(s)                                                              | `[]`                                 |
| `platformCortex.sidecars`                           | Add additional sidecar containers to the Conduktor Console Cortex pod(s)                                                                                            | `[]`                                 |
| `platformCortex.initContainers`                     | Add additional init containers to the Conduktor Console Cortex pod(s)                                                                                               | `[]`                                 |
| `platformCortex.service.type`                       | Conduktor Console Cortex service type                                                                                                                               | `ClusterIP`                          |
| `platformCortex.service.ports.cortex`               | Conduktor Console Cortex service HTTP port                                                                                                                          | `9009`                               |
| `platformCortex.service.ports.alertmanager`         | Conduktor Console Cortex AlertManager service HTTP port                                                                                                             | `9010`                               |
| `platformCortex.service.ports.prometheus`           | Conduktor Console Cortex Prometheus service HTTP port                                                                                                               | `9090`                               |
| `platformCortex.service.nodePorts.cortex`           | Node port for Cortex HTTP                                                                                                                                           | `""`                                 |
| `platformCortex.service.nodePorts.alertmanager`     | Node port for AlertManager HTTP                                                                                                                                     | `""`                                 |
| `platformCortex.service.nodePorts.prometheus`       | Node port for Prometheus HTTP                                                                                                                                       | `""`                                 |
| `platformCortex.service.clusterIP`                  | Conduktor Console Cortex service Cluster IP                                                                                                                         | `""`                                 |
| `platformCortex.service.loadBalancerSourceRanges`   | Conduktor Console Cortex service Load Balancer sources                                                                                                              | `[]`                                 |
| `platformCortex.service.externalTrafficPolicy`      | Conduktor Console Cortex service external traffic policy                                                                                                            | `Cluster`                            |
| `platformCortex.service.labels`                     | Additional custom labels for Conduktor Console Cortex service                                                                                                       | `{}`                                 |
| `platformCortex.service.annotations`                | Additional custom annotations for Conduktor Console Cortex service                                                                                                  | `{}`                                 |
| `platformCortex.service.extraPorts`                 | Extra ports to expose in Conduktor Console Cortex service (normally used with the `sidecars` value)                                                                 | `[]`                                 |
| `platformCortex.service.sessionAffinity`            | Control where client requests go, to the same pod or round-robin                                                                                                    | `None`                               |
| `platformCortex.service.sessionAffinityConfig`      | Additional settings for the sessionAffinity                                                                                                                         | `{}`                                 |
| `platformCortex.service.extraSpecs`                 | Extra specs for the service to be added under `spec` key                                                                                                            | `{}`                                 |

## Snippets

### Console configuration

If you are looking for additional snippets related to the configuration of
console, we recommend you to look at our
[documentation](https://docs.conduktor.io/platform/configuration/configuration-snippets/).

- [Install with a basic SSO configuration](#install-with-a-basic-sso-configuration)
- [Install with a registered Kafka cluster](#install-with-a-kafka-cluster)
- [Install with a Confluent Cloud cluster](#install-with-a-confluent-cloud-cluster)
- [Install with an enterprise license](#install-with-an-enterprise-license)
- [Install without Conduktor monitoring](#install-without-conduktor-monitoring)

### Kubernetes configuration
- [Install with an enterprise license](#install-with-an-enterprise-license)
- [Install with a basic SSO configuration](#install-with-a-basic-sso-configuration)
- [Install with a Kafka cluster](#install-with-a-kafka-cluster)
- [Install with a Confluent Cloud cluster](#install-with-a-confluent-cloud-cluster)
- [Install without Conduktor monitoring](#install-without-conduktor-monitoring)
- [Provide the license as a Kubernetes Secret](#provide-the-license-as-a-kubernetes-secret)
- [Provide credentials configuration as a Kubernetes Secret](#provide-credentials-configuration-as-a-kubernetes-secret)
- [Provide monitoring configuration as a Kubernetes Secret](#provide-monitoring-configuration-as-a-kubernetes-secret)
- [Pulling from private registry using `global.imagePullSecrets`](#pulling-from-private-registry-using-globalimagepullsecrets)
- [Store platform data into a Persistent Volume](#store-platform-data-into-a-persistent-volume)
- [Install with a PodAffinity](#install-with-a-podaffinity)
- [Provide console configuration as a Kubernetes ConfigMap](#provide-console-configuration-as-a-kubernetes-configmap)
- [Provide additional credentials as a Kubernetes Secret](#provide-additional-credentials-as-a-kubernetes-secret)
- [Install with a toleration](#install-with-a-toleration)
- [Ingress configuration](#ingress-configuration)
  - [Ingress TLS configuration](#ingress-tls-configuration)
    - [Using cert-manager](#using-cert-manager)
    - [Using existing TLS secret](#using-existing-tls-secret)
    - [Using plain PEM certificate and key](#using-plain-pem-certificate-and-key)
    - [Using Multiple TLS secrets](#using-multiple-tls-secrets)
    - [Using Helm generated self-signed certificates](#using-helm-generated-self-signed-certificates)
  - [Ingress with context path](#ingress-with-context-path)
- [Container TLS configuration](#container-tls-configuration)
  - [Use an existing secret](#use-an-existing-secret-)
  - [Install with Self-Signed TLS certificate](#install-with-self-signed-tls-certificate)
- [Install with a custom service account](#install-with-a-custom-service-account)
- [Install with a AWS EKS IAM Role](#install-with-a-aws-eks-iam-role)
- [Install with Console technical monitoring](#install-with-console-technical-monitoring)
- [Install with custom certificates or keytab](#install-with-custom-certificates-or-keytab)

### Install with an enterprise license

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "<admin_email>"
    password: "<admin_password>"

  database:
    hosts:
      - host: "<postgres_host>"
        port: 5432
    name: "<postgres_database>"
    username: "<postgres_username>"
    password: "<postgres_password>"
    # or you can provide a full database URL
    # url: "jdbc:postgresql://<user>:<password>@<server1>:<port>/<dbname>"

  license: "<ENTERPRISE_LICENSE>"
```
License can also be passed as environment variable named `CDK_LICENSE` from a secret using either `existingLicenseSecret` that expect a key named `CDK_LICENSE` or `extraEnvVars` or `extraEnvVarsSecret`.

### Install with a basic SSO configuration

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "<admin_email>"
    password: "<admin_password>"

  database:
    hosts:
      - host: "<postgres_host>"
        port: 5432
    name: "<postgres_database>"
    username: "<postgres_username>"
    password: "<postgres_password>"

  sso:
    oauth2:
      - name: "<idp-id>"
        default: true
        client-id: "<client_id>"
        client-secret: "<client_secret>"
        callback-uri: "http://localhost/auth/oauth/callback/<idp-id>"
        openid:
          issuer: "https://idp-host.com/"

  license: "<license_key>"
```
More details on SSO configuration can be found in our [documentation](https://docs.conduktor.io/guide/conduktor-in-production/deploy-artifacts/deploy-console/env-variables#sso-properties).

### Install with a Kafka cluster

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "<admin_email>"
    password: "<admin_password>"

  database:
    hosts:
      - host: "<postgres_host>"
        port: 5432
    name: "<postgres_database>"
    username: "<postgres_username>"
    password: "<postgres_password>"

  clusters:
    - id: my-local-kafka-cluster
      name: My Local Kafka Cluster
      color: "#0013E7"
      bootstrapServers: "my-bootstrap-server:9092"
      schemaRegistry:
        id: my-schema-registry
        url: "http://my-schema-registry:8081"
```

### Install with a Confluent Cloud cluster

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "<admin_email>"
    password: "<admin_password>"

  database:
    hosts:
      - host: "<postgres_host>"
        port: 5432
    name: "<postgres_database>"
    username: "<postgres_username>"
    password: "<postgres_password>"

  clusters:
    - id: confluent-cloud-cluster
      name: Confluent Cloud Cluster
      color: "#0013E7"
      bootstrapServers: pkc-xxxxx.region.provider.confluent.cloud:9092
      properties: |
        sasl.mechanism=PLAIN
        security.protocol=SASL_SSL
        sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="YOUR_API_KEY" password="YOUR_API_SECRET";
      schemaRegistry:
        id: confluent-cloud-sr
        url: https://psrc-xxxxx.region.provider.confluent.cloud
        properties: |
          basic.auth.credentials.source=USER_INFO
          basic.auth.user.info=SR_API_KEY:SR_API_SECRET
```

### Install without Conduktor monitoring

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "<admin_email>"
    password: "<admin_password>"

  database:
    hosts:
      - host: "<postgres_host>"
        port: 5432
    name: "<postgres_database>"
    username: "<postgres_username>"
    password: "<postgres_password>"

platformCortex:
  enabled: false
```

### Provide the license as a Kubernetes Secret

This snippet expects that a _Kubernetes Secret Resource_ already exists inside
your cluster with a key named `CDK_LICENSE` containing your license key.

```yaml
# values.yaml
config:
  organization:
    name: "<your_org_name>"

  admin:
    email: "<your_admin_email>"
    password: "<your_admin_password>"

  database:
    host: "<postgres_host>"
    port: 5432
    name: "<postgres_database>"
    username: "<postgres_username>"
    password: "<postgres_password>"

  existingLicenseSecret: "<your_secret_name>"
```

### Provide credentials configuration as a Kubernetes Secret

We expect the secret to contain the following keys:

- "`CDK_ORGANIZATION_NAME`": name of the organization
- "`CDK_ADMIN_EMAIL`" : email of the admin user
- "`CDK_ADMIN_PASSWORD`" : password of the admin user
- "`CDK_DATABASE_PASSWORD`": password of the database
- "`CDK_DATABASE_USERNAME`": username of the database
- Optional: "`CDK_DATABASE_URL`": full database URL, if not provided we will build it using the other parameters. If you provide this parameter, the `CDK_DATABASE_HOST`, `CDK_DATABASE_PORT` and `CDK_DATABASE_NAME` parameters will be ignored.

```yaml
# values.yaml
config:
  existingSecret: "<your_secret_name>"
  database:
    host: ""
    port: 5432
    name: "postgres"
```

```yaml
# secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: "<your_secret_name>"
type: Opaque
data:
  CDK_ORGANIZATION_NAME: <your_organization_name>
  CDK_ADMIN_EMAIL: <your_admin_email>
  CDK_ADMIN_PASSWORD: <your_admin_password>
  CDK_DATABASE_PASSWORD: <your_database_password>
  CDK_DATABASE_USERNAME: <your_database_username>
  # CDK_DATABASE_URL: jdbc:postgresql://<user>:<password>@<server1>:<port>/<dbname>  # Optional
```

### Provide monitoring configuration as a Kubernetes Secret

We expect the secret to contain the following keys:

- For S3 like storage:
  - "CDK_MONITORING_STORAGE_S3_ACCESSKEYID" : S3 access key
  - "CDK_MONITORING_STORAGE_S3_SECRETACCESSKEY" : S3 secret access key
- For GCS like storage:
  - "CDK_MONITORING_STORAGE_GCS_SERVICEACCOUNT" : GCS service account JSON representing either client_credentials.json file or a service account key file.
- For Azure like storage:
  - "CDK_MONITORING_STORAGE_AZURE_ACCOUNTNAME" : Azure account name
  - "CDK_MONITORING_STORAGE_AZURE_ACCOUNTKEY" : Azure account key
- For Swift like storage:
  - "CDK_MONITORING_STORAGE_SWIFT_PASSWORD" : Swift user password
  - "CDK_MONITORING_STORAGE_SWIFT_USERID" OR "CDK_MONITORING_STORAGE_SWIFT_USERNAME": Swift user id or name

```yaml
# values.yaml
monitoringConfig:
  existingSecret: "<your_secret_name>"
  storage:
    s3:
      endpoint: "s3.eu-west-1.amazonaws.com"
      bucket: "conduktor"
```

```yaml
# secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: "<your_secret_name>"
type: Opaque
data:
  CDK_MONITORING_STORAGE_S3_ACCESSKEYID: <your_s3_access_key>
  CDK_MONITORING_STORAGE_S3_SECRETACCESSKEY: <your_s3_secret_access_key>
```


### Pulling from private registry using `global.imagePullSecrets`

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

Then in your `values.yaml` file, you can set the `global.imagePullSecrets` parameter to the name of the secret you created, you will also need to modify the `global.imageRegistry` parameters to use the same registry as the secret you created.

The below example shows how to set the `global.imagePullSecrets` parameter and the `global.imageRegistry` parameters to use a private registry:
```yaml
global:
  imageRegistry: regsitry.company.io
  imagePullSecrets:
    - docker-regsitry-secret

platform:
  image:
    repository: conduktor/conduktor-console
    tag: nightly

platformCortex:
  image:
    repository: conduktor/conduktor-console-cortex
    tag: nightly
```

You can also specify the `global.imagePullSecrets` and `global.imageRegistry` parameters in the `platform` and `platformCortex` sections if you want to use different secrets and registries for each of them.

```yaml
platform:
  image:
    registry: regsitry.company.io
    repository: conduktor/conduktor-console
    tag: nightly
    pullSecrets:
      - docker-regsitry-secret

platformCortex:
  image:
    registry: regsitry.company.io
    repository: conduktor/conduktor-console-cortex
    tag: nightly
    pullSecrets:
      - docker-regsitry-secret-cortex
```

### Store platform data into a Persistent Volume

```yaml
# values.yaml
config:
  organization:
    name: "<your_org_name>"

  admin:
    email: "<your_admin_email>"
    password: "<your_admin_password>"

  database:
    host: "<postgres_host>"
    port: 5432
    name: "<postgres_database>"
    username: "<postgres_username>"
    password: "<postgres_password>"

platform:
  dataVolume:
    persistentVolumeClaim:
      claimName: data-pv-claim
  tmpVolume:
    persistentVolumeClaim:
      claimName: tmp-pv-claim

platformCortex:
  enabled: true
  dataVolume:
    persistentVolumeClaim:
      claimName: monitoring-data-pv-claim
  tmpVolume:
    persistentVolumeClaim:
      claimName: monitoring-tmp-pv-claim
```

### Install with a PodAffinity

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "admin@my-org.com"
    password: "admin"

  database:
    host: ""
    port: 5432
    name: "postgres"
    username: ""
    password: ""

platform:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        - labelSelector:
            matchExpressions:
              - key: security
                operator: In
                values:
                  - S1
          topologyKey: topology.kubernetes.io/zone

platformCortex:
  enabled: true
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        - labelSelector:
            matchExpressions:
              - key: security
                operator: In
                values:
                  - S1
          topologyKey: topology.kubernetes.io/zone
```

### Provide console configuration as a Kubernetes ConfigMap

**NOTE:** We recommend to be using a secret (see [snippet](#provide-credentials-configuration-as-a-kubernetes-secret))
in addition to the ConfigMap in order to protect your credentials.

The ConfigMap is expected to contain a key `platform-config.yaml` which got
the console configuration in YAML format.

```yaml
# values.yaml
config:
  # We highly recommend you to be using both the secret and the ConfigMap
  # check our snippet 'Provide credentials configuration as a Kubernetes Secret'
  existingSecret: "<your_secret_name>"

platform:
  existingConfigmap: "<your_configmap_name>"
```

```yaml
# platform-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: "<your_configmap_name>"
data:
  platform-config.yaml: |
    database:
      host: '<postgres_host>'
      port: 5432
      name: '<postgres_database>'
```

### Provide additional credentials as a Kubernetes Secret

In case our helm chart doesn't protect all the credentials you need, you can
use this method to provide additional credentials through a Kubernetes
Secret Resource you previously created. You can have this case for LDAP
credentials, or for SSO credentials for example.

The keys of your secret will be used as environment variables in the
console pod. Be sure to check available [environment variables](https://docs.conduktor.io/platform/configuration/env-variables/)
in our documentation.

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "admin@my-org.com"
    password: "admin"

  database:
    host: ""
    port: 5432
    name: "postgres"
    username: ""
    password: ""

platform:
  extraEnvVarsSecret: "<your_secret_name>"
platformCortex:
  extraEnvVarsSecret: "<your_secret_name>"
```

### Install with a toleration

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "admin@my-org.com"
    password: "admin"

  database:
    host: ""
    port: 5432
    name: "postgres"
    username: ""
    password: ""

  platform:
    external:
      url: "https://platform.local"
    https:
      selfSigned: true
platform:
  tolerations:
    - key: "donotschedule"
      operator: "Exists"
      effect: "NoSchedule"

platformCortex:
  enabled: true
  tolerations:
    - key: "donotschedule"
      operator: "Exists"
      effect: "NoSchedule"
```

### Ingress configuration

#### Ingress TLS configuration

##### Using cert-manager
This solution leverage [cert-manager](https://cert-manager.io/docs/) to generate TLS certificates for your ingress simply using annotations.

Example using a [Nginx Ingress](https://kubernetes.github.io/ingress-nginx/) and cert-manager with [Let's Encrypt](https://cert-manager.io/docs/tutorials/acme/pomerium-ingress/#configure-lets-encrypt-issuer) issuer :
```yaml
ingress:
  enabled: true
  hostname: conduktor-console.my-domain.com
  ingressClassName: <ingress-class-name>
  tls: true
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-issuer
    kubernetes.io/ingress.class: nginx
```

##### Using existing TLS secret
If you already have a TLS secret of type `kubernetes.io/tls` created in your cluster, you can use it in your ingress configuration.

```yaml
ingress:
  enabled: true
  hostname: conduktor-console.my-domain.com
  ingressClassName: <ingress-class-name>
  tls: true
  secrets:
    - name: my-existing-tls-secret
```
OR using `ingress.extraTls`
```yaml
ingress:
  enabled: true
  hostname: conduktor-console.my-domain.com
  ingressClassName: <ingress-class-name>
  tls: true
  extraTls:
    - secretName: my-existing-tls-secret
      hosts:
        - conduktor-console.my-domain.com
```

##### Using plain PEM certificate and key

If you have a PEM certificate and key, you can use them directly in your `values.yaml` file.
```yaml
ingress:
  enabled: true
  hostname: conduktor-console.my-domain.com
  ingressClassName: <ingress-class-name>
  tls: true
  secrets:
    - name: my-new-tls-secret
      certificate: |-
        -----BEGIN CERTIFICATE-----
        ...
        -----END CERTIFICATE-----
      key: |-
        -----BEGIN PRIVATE KEY-----
        ...
        -----END PRIVATE KEY-----
```

##### Using Multiple TLS secrets

If using multiple hostnames, you can use the `extraTls` parameter to add more TLS secrets.

```yaml
ingress:
  enabled: true
  hostname: conduktor-console.my-domain.com
  ingressClassName: <ingress-class-name>
  tls: true
  extraHosts:
    - host: my-other-hostname.com
      path: /
      pathType: ImplementationSpecific
  extraTls:
    - secretName: conduktor-console.my-domain.com-tls
      hosts:
        - conduktor-console.my-domain.com
    - secretName: my-other-hostname.com-tls
      hosts:
        - my-other-hostname.com
```

##### Using Helm generated self-signed certificates
This solution use Helm [`genCA`](https://helm.sh/docs/chart_template_guide/function_list/#genca), [`genSignedCert`](https://helm.sh/docs/chart_template_guide/function_list/#gensignedcert) functions to generate self-signed certificates for your ingress. (Not for production use)
```yaml
ingress:
  enabled: true
  hostname: conduktor-console.my-domain.com
  ingressClassName: <ingress-class-name>
  tls: true
  selfSigned: true
```
It will generate a secret name `<hostname>-tls` with the certificates and key.

#### Ingress with context path

Starting Console version 1.41.0, you can configure an ingress with a context path.

Example using `/console` as context path for and Nginx Ingress controller:
```yaml
config:
  platform:
    external:
      url: "https://conduktor.my-domain.com/console" # Note the /console path here is needed for proper redirects
ingress:
  enabled: true
  hostname: conduktor.my-domain.com
  ingressClassName: nginx # example with nginx ingress
  tls: true
  path: /console(/|$)(.*)
  pathType: ImplementationSpecific
  annotations:
    # For Nginx Ingress controller only
    nginx.ingress.kubernetes.io/rewrite-target: /$2
```

> Note: Depending on your ingress controller, you may need to add specific annotations and path to handle the context path properly. Please refer to your ingress controller documentation for more details.

### Container TLS configuration

#### Use an existing secret

If you already have a TLS secret of type `kubernetes.io/tls` created in your cluster, you can use it in your platform configuration.
At startup Console will look for a `tls.crt` and `tls.key` PEM inside the secret to be mounted.

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "admin@my-org.com"
    password: "admin"

  database:
    host: ""
    port: 5432
    name: "postgres"
    username: ""
    password: ""

  platform:
    external:
      url: "https://platform.local"
    https:
      selfSigned: false
      existingSecret: "platform-tls"
```

#### Install with Self-Signed TLS certificate

This solution use Helm[`genCA`](https://helm.sh/docs/chart_template_guide/function_list/#genca), [`genSignedCert`](https://helm.sh/docs/chart_template_guide/function_list/#gensignedcert) functions to generate self-signed certificates using `config.platform.external.url` for the certificate subject name CN. (Not for production use)

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "admin@my-org.com"
    password: "admin"

  database:
    host: ""
    port: 5432
    name: "postgres"
    username: ""
    password: ""

  platform:
    external:
      url: "https://platform.local"
    https:
      selfSigned: true
```
Self signed secret will be stored inside a secret named `<fullname>-platform-tls`.

### Install with a custom service account

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "admin@my-org.com"
    password: "admin"

  database:
    host: ""
    port: 5432
    name: "postgres"
    username: ""
    password: ""

serviceAccount:
  create: false
  name: "my-service-account"
```

### Install with a AWS EKS IAM Role

**NOTE:** Service account are shared between Conduktor Console and Cortex pods.

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "admin@my-org.com"
    password: "admin"

  database:
    host: ""
    port: 5432
    name: "postgres"
    username: ""
    password: ""

serviceAccount:
  annotations:
    eks.amazonaws.com/role-arn: "arn:aws:iam::123456789012:role/my-role"
```

### Install with Console technical monitoring

If you want to enable the technical monitoring of Conduktor Console, you can enable built-in Prometheus metrics collector and Grafana dashboard.
But to work you need to have [prometheus-operator](https://github.com/prometheus-operator/prometheus-operator) and [grafana-operator](https://grafana.github.io/grafana-operator/docs/installation/helm/) installed in your cluster.
We use following CRDs from these operators:

- **ServiceMonitor** : `monitoring.coreos.com/v1/ServiceMonitor`
- **GrafanaDashboard** : `grafana.integreatly.org/v1beta1/GrafanaDashboard` (v5) or `integreatly.org/v1alpha1/GrafanaDashboard` (v4)
- **GrafanaFolder** : `grafana.integreatly.org/v1beta1/GrafanaFolder` (v5 only)

You can also manually install Grafana dashboard from Json export located here [console.json](./grafana-dashboards/console.json).
It takes two inputs variables:

- `DS_PROMETHEUS` : Prometheus Datasource name
- `VAR_NAMESPACE` : Namespace where Conduktor Console is installed

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "admin@my-org.com"
    password: "admin"

  database:
    host: ""
    port: 5432
    name: "postgres"
    username: ""
    password: ""

platform:
  metrics:
    enabled: true
    serviceMonitor:
      enabled: true
      namespace: "monitoring-namespace"
      labels:
        monitor: "1"
      interval: "30s"
      scrapeTimeout: "10s"
    grafana:
      enabled: true
      namespace: "monitoring-namespace"
      folder: "tools"
      matchLabels:
        grafana: "tooling"
      labels:
        grafana_dashboard: "1"
      datasources:
        prometheus: "my-prometheus-ds"
```

This example will install a `ServiceMonitor` and a `GrafanaDashboard` in the namespace `monitoring-namespace`.
The `ServiceMonitor` will scrape metrics from Conduktor Console every 30 seconds and the `GrafanaDashboard` will be available in Grafana instance with label `grafana: tooling` in the folder `tools` and use Prometheus datasource named `my-prometheus-ds`.

### Install with custom certificates or keytab
*NOTE:* The example is for a `keytab` but the same technique could be applied if you need to configure an additional `truststore` or `keystore`.

It's recommended to load your certificates and keytab as secrets.
```shell
kubectl create secret generic conduktor-console-keytab \
    --from-file=./my.keytab
```

We can then proceed to mount the secret as a volume.
Note the `mountPath` which is where your cert will be accessible from.
```yaml
platform:
  extraVolumes:
    - name: kafka-keytab
      secret:
        secretName: conduktor-console-keytab
  extraVolumeMounts:
    - name: kafka-keytab
      readonly: true
      mountPath: /etc/kafka
```

Finally, your cluster configuration should look something like this:
```yaml
config:
  clusters:
    - id: my-cluster
      bootstrapServers: kafka:9092
      properties: |
          sasl.jaas.config=com.sun.security.auth.module.Krb5LoginModule required useKeyTab=true storeKey=true keyTab="/etc/kafka/my.keytab" principal="admin/for-kafka@TEST.CONDUKTOR.IO";
          sasl.mechanism=GSSAPI
          security.protocol=SASL_SSL
          sasl.kerberos.service.name=kafka
```

If you need to mount the truststore you will probably need the [additional properties](https://docs.conduktor.io/platform/get-started/configuration/configuration-snippets/#2-way-ssl-keystore--truststore):
```shell
ssl.truststore.type=JKS
ssl.truststore.location=/etc/kafka/my-truststore.jks
ssl.truststore.password=conduktor
```

Alternatively, to extend the global default (JVM) truststore (see also [Define Console environment variables](https://docs.conduktor.io/guide/conduktor-in-production/deploy-artifacts/deploy-console/env-variables#docker-image-environment-variables)):

```shell
kubectl create secret generic tls-truststore \
   --from-file=truststore.jks=$TLSDIR/truststore.jks \
   --dry-run=client \
   -o json | kubectl apply -f -
```

```yaml
platform:
  extraEnvVars:
    - name: CDK_SSL_TRUSTSTORE_PATH
      value: '/mnt/truststore/truststore.jks'
    - name: CDK_SSL_TRUSTSTORE_PASSWORD
      value: 'changeit'
    - name: CDK_SSL_TRUSTSTORE_TYPE
      value: 'jks'
  extraVolumes:
    - name: truststore
      secret:
        secretName: tls-truststore
  extraVolumeMounts:
    - name: truststore
      readonly: true
      mountPath: /mnt/truststore
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Troubleshooting

For guides and advanced help, please refer to our
[documentation](https://docs.conduktor.io/platform/installation/get-started/kubernetes),
or to our charts `README`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
