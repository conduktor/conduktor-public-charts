# Platform-controller

> If you have any questions or [feedback](https://product.conduktor.help/c/55-helm-chart) contact our [support](https://www.conduktor.io/contact/support/).

## Introduction

Controller to deploy the Conduktor Platform on Kubernetes.

## Prerequisites

- Kubernetes 1.16+
- Helm 3.1.0+

## Configure Conduktor Helm repository

```console
$ helm repo add conduktor https://helm.conduktor.io
$ helm search repo conduktor
```

## Run the Platform controller

To install the chart with the release name `platform`:

```console
$ helm install -n conduktor --create-namespace platform conduktor/platform-controller \
   --set platform.config.organization=YOUR_ORGANIZATION \
   --set platform.config.adminEmail=admin@yourdomain.com \
   --set platform.config.adminPassword=TOP_SECRET
```

Note that organization, adminEmail and adminPassword are mandatory.

### With enterprise license

```console
$ helm install -n conduktor --create-namespace platform conduktor/platform-controller \
   --set platform.config.license=YOUR_LICENSE \
   --set platform.config.organization=YOUR_ORGANIZATION \
   --set platform.config.adminEmail=admin@yourdomain.com \
   --set platform.config.adminPassword=TOP_SECRET
```

## Versions matrix

See [compatibility matrix](https://docs.conduktor.io/platform/installation/get-started/kubernetes/#versions-compatibility-matrix) for more details.
To know which version of this chart deploy which version of the Conduktor.

## Architecture

This Helm chart will deploy the Platform-controller that is responsible to deploy the Conduktor Platform on the same namespace.

Optionally it can deploy a Postgresql and/or a Kafka cluster inside the same namespace for demo purpose.

More details on the [documentation](https://docs.conduktor.io/platform/installation/get-started/kubernetes/#architecture).

## Parameters

### Global parameters

| Name                      | Description                              | Value |
| ------------------------- | ---------------------------------------- | ----- |
| `global.imageRegistry`    | Global Docker image registry             | `""`  |
| `global.imagePullSecrets` | Docker login secrets name for image pull | `[]`  |


### Controller parameters

Conduktor Controller parameters

| Name                                                             | Description                                                                   | Value                           |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------- |
| `controller.tolerations`                                         | Tolerations for pod assignment                                                | `[]`                            |
| `controller.image.registry`                                      | Platform Controller image registry                                            | `docker.io`                     |
| `controller.image.repository`                                    | Platform Controller image repository                                          | `conduktor/platform-controller` |
| `controller.image.pullPolicy`                                    | Platform Controller image pull policy                                         | `Always`                        |
| `controller.image.tag`                                           | Platform Controller image tag                                                 | `0.12.1`                        |
| `controller.commonLabels`                                        | Common labels to add to all resources                                         | `{}`                            |
| `controller.securityContext`                                     | Optionally specify some Security Context.                                     | `{}`                            |
| `controller.commonAnnotations`                                   | Common annotations to add to all resources                                    | `{}`                            |
| `controller.serviceAccount.create`                               | Create Kubernetes service account.                                            | `true`                          |
| `controller.serviceAccount.name`                                 | Service account name override                                                 | `conduktor-controller`          |
| `controller.resources.limits.cpu`                                | CPU limit for the platform controller                                         | `100m`                          |
| `controller.resources.limits.memory`                             | Memory limit for the platform controller                                      | `128Mi`                         |
| `controller.resources.requests.cpu`                              | CPU resource requests for platform controller                                 | `100m`                          |
| `controller.resources.requests.memory`                           | Memory resource requests for platform controller                              | `128Mi`                         |
| `controller.ingress.enabled`                                     | Enable ingress controller resource                                            | `false`                         |
| `controller.ingress.ingressClassName`                            | Ingress class name for the controller                                         | `""`                            |
| `controller.ingress.host`                                        | Platform controller Host                                                      | `controller.local`              |
| `controller.ingress.extraHosts`                                  | An array with additional hostname(s) to be covered with this ingress record.  | `[]`                            |
| `controller.ingress.tls.enabled`                                 | Enable TLS for the controller ingress                                         | `false`                         |
| `controller.ingress.tls.host`                                    | Host                                                                          | `nil`                           |
| `controller.ingress.tls.secretRef`                               | Secret name with keystore to load                                             | `""`                            |
| `controller.ingress.annotations`                                 | Additional annotations for the ingress                                        | `{}`                            |
| `controller.service.annotations`                                 | Annotations for controller service                                            | `{}`                            |
| `controller.service.http.port`                                   | HTTP port                                                                     | `8080`                          |
| `controller.extraEnvVars`                                        | Array with extra environment variables                                        | `[]`                            |
| `controller.extraEnvVarsCM`                                      | Name of existing ConfigMap containing extra env vars                          | `""`                            |
| `controller.extraEnvVarsSecret`                                  | Name of existing Secret containing extra env vars                             | `""`                            |
| `controller.metrics.prometheus.serviceMonitor.enabled`           | Enable ServiceMonitor prometheus operator configuration for metrics scrapping | `false`                         |
| `controller.metrics.prometheus.serviceMonitor.metricRelabelings` | Specify additional relabeling of metrics                                      | `[]`                            |
| `controller.metrics.prometheus.serviceMonitor.relabelings`       | Specify general relabeling                                                    | `[]`                            |
| `controller.podAnnotations`                                      | Map of annotations to add to the controller pods                              | `{}`                            |
| `controller.affinity`                                            | Affinity for pod assignment of the controller                                 | `{}`                            |


### Platform parameters

Conduktor Platform parameters

| Name                                              | Description                                                                                                                                       | Value            |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| `platform.tolerations`                            | Tolerations for pod assignment.                                                                                                                   | `[]`             |
| `platform.commonLabels`                           | Common labels to add to all resources                                                                                                             | `{}`             |
| `platform.image`                                  | Optionally specify an image to use for the platform.                                                                                              | `{}`             |
| `platform.image.registry`                         | Platform image registry                                                                                                                           |                  |
| `platform.image.repository`                       | Platform image repository                                                                                                                         |                  |
| `platform.image.tag`                              | Platform image tag. The major and minor version must be compatible with the platform version that is supported by the current controller version. |                  |
| `platform.ignoreImageConstraints`                 | When `true` allows the use of any tag and bypasses the constraint on tag versions.                                                                | `false`          |
| `platform.securityContext`                        | Optionally specify some Security Context.                                                                                                         | `{}`             |
| `platform.affinity`                               | Affinity for pod assignment of the platform                                                                                                       | `{}`             |
| `platform.serviceAccount.name`                    | Name of the service account that will be used by the platform                                                                                     | `""`             |
| `platform.existingSecret`                         | Existing secret for platform                                                                                                                      | `""`             |
| `platform.service.type`                           | Kubernetes service type. Only support ClusterIP or NodePort                                                                                       | `ClusterIP`      |
| `platform.service.name`                           | Name of the platform service                                                                                                                      | `platform`       |
| `platform.service.annotations`                    | Annotations for platform service                                                                                                                  | `{}`             |
| `platform.service.ports.platform`                 | Platform service port                                                                                                                             | `80`             |
| `platform.service.nodePorts.platform`             | Specify the platform nodePort for the NodePort service type                                                                                       | `""`             |
| `platform.service.clusterIP`                      | Specify the service IP for the ClusterIP service type                                                                                             | `""`             |
| `platform.config.replicas`                        | Number of replicas for the platform controller                                                                                                    | `1`              |
| `platform.config.name`                            | Name of the platform controller                                                                                                                   | `platform`       |
| `platform.config.organization`                    | Your organizations name (mandatory)                                                                                                               | `""`             |
| `platform.config.adminEmail`                      | Email of the admin user (mandatory)                                                                                                               | `""`             |
| `platform.config.adminPassword`                   | Password of the admin user (mandatory)                                                                                                            | `""`             |
| `platform.config.external_url`                    | Force platform external URL, useful for SSO callback URL when using reverse proxy.                                                                | `""`             |
| `platform.config.containerPorts.platform`         | Platform exposed and listening port                                                                                                               | `8080`           |
| `platform.config.modules.console`                 | Enable or disable the console module                                                                                                              | `true`           |
| `platform.config.modules.data_masking`            | Enable or disable the data masking module                                                                                                         | `true`           |
| `platform.config.modules.monitoring`              | Enable or disable the monitoring module                                                                                                           | `true`           |
| `platform.config.modules.testing`                 | Enable or disable the testing module                                                                                                              | `false`          |
| `platform.config.modules.governance`              | Enable or disable the governance module                                                                                                           | `true`           |
| `platform.config.monitoring.storage.s3.bucket`    | S3 bucket name                                                                                                                                    | `""`             |
| `platform.config.monitoring.storage.s3.endpoint`  | S3 endpoint                                                                                                                                       | `""`             |
| `platform.config.monitoring.storage.s3.accessKey` | S3 access key                                                                                                                                     | `""`             |
| `platform.config.monitoring.storage.s3.secretKey` | S3 secret key                                                                                                                                     | `""`             |
| `platform.config.monitoring.storage.s3.region`    | S3 region                                                                                                                                         | `""`             |
| `platform.config.monitoring.storage.s3.insecure`  | S3 insecure                                                                                                                                       | `true`           |
| `platform.config.sso.enabled`                     | Enable or disable the SSO (only on enterprise plan)                                                                                               | `false`          |
| `platform.config.sso.ignoreUntrustedCertificate`  | Disable SSL checks                                                                                                                                | `false`          |
| `platform.config.sso.ldap.name`                   | LDAP connection name                                                                                                                              | `""`             |
| `platform.config.sso.ldap.server`                 | LDAP server host and port                                                                                                                         | `""`             |
| `platform.config.sso.ldap.managerDn`              | Sets the manager DN                                                                                                                               | `""`             |
| `platform.config.sso.ldap.managerPassword`        | Sets the manager password                                                                                                                         | `""`             |
| `platform.config.sso.ldap.searchBase`             | Sets the base DN to search                                                                                                                        | `""`             |
| `platform.config.sso.ldap.groups.enabled`         | Sets if group search is enabled                                                                                                                   | `false`          |
| `platform.config.sso.ldap.groups.base`            | Sets the base DN to search from                                                                                                                   | `""`             |
| `platform.config.sso.ldap.groups.filter`          | Sets the group search filter                                                                                                                      | `""`             |
| `platform.config.sso.oauth2.name`                 | OAuth2 connection name                                                                                                                            | `""`             |
| `platform.config.sso.oauth2.default`              | Use as default                                                                                                                                    | `true`           |
| `platform.config.sso.oauth2.clientId`             | OAuth2 client id                                                                                                                                  | `""`             |
| `platform.config.sso.oauth2.clientSecret`         | OAuth2 client secret                                                                                                                              | `""`             |
| `platform.config.sso.oauth2.openid.issuer`        | Issuer to check on token                                                                                                                          | `""`             |
| `platform.config.license`                         | Enterprise license key. If not provided, fallback to free plan.                                                                                   | `""`             |
| `platform.config.database`                        | Database configuration. If postgresql.enable is true, it will configure the database with postgresql.auth values                                  |                  |
| `platform.config.database.host`                   | Database host. If postgresql.enable is true, it will configure the database host to the postgresql pod name. e.g: platform-postgresql             | `""`             |
| `platform.config.database.port`                   | Database port                                                                                                                                     | `5432`           |
| `platform.config.database.username`               | Database user. If postgresql.enable is true, it will take the postgresql.auth.username value                                                      | `""`             |
| `platform.config.database.password`               | Database password, can be a string or can reference a secret. If postgresql.enable is true, it will take the postgresql.auth.password value       | `""`             |
| `platform.config.database.name`                   | Database name. If postgresql.enable is true, it will take the postgresql.auth.database value                                                      | `postgres`       |
| `platform.config.tls.enabled`                     | Enable TLS for the platform (at pod level)                                                                                                        | `false`          |
| `platform.config.tls.cert`                        | Raw TLS certificate                                                                                                                               | `""`             |
| `platform.config.tls.key`                         | Raw TLS certificate                                                                                                                               | `""`             |
| `platform.config.tls.existingSecret`              | Secret name with certificate (must have keys: tls.crt, tls.key)                                                                                   | `""`             |
| `platform.extraEnvVars`                           | Array with extra environment variables                                                                                                            | `[]`             |
| `platform.extraEnvVarsCM`                         | Name of existing ConfigMap containing extra env vars                                                                                              | `""`             |
| `platform.extraEnvVarsSecret`                     | Name of existing Secret containing extra env vars                                                                                                 | `""`             |
| `platform.ingress.enabled`                        | Enable ingress platform resource                                                                                                                  | `false`          |
| `platform.ingress.ingressClassName`               | Ingress class name for the platform                                                                                                               | `""`             |
| `platform.ingress.host`                           | Platform host                                                                                                                                     | `platform.local` |
| `platform.ingress.tls.enabled`                    | Enable Platform TLS                                                                                                                               | `false`          |
| `platform.ingress.tls.host`                       | Platform Host                                                                                                                                     | `nil`            |
| `platform.ingress.tls.secretRef`                  | Secret name with keystore to load                                                                                                                 | `""`             |
| `platform.ingress.annotations`                    | Additional annotations for the ingress                                                                                                            | `{}`             |
| `platform.resources.limits.cpu`                   | CPU limit for the platform container                                                                                                              | `4000m`          |
| `platform.resources.limits.memory`                | Memory limit for the container                                                                                                                    | `8Gi`            |
| `platform.resources.requests.cpu`                 | CPU resource requests                                                                                                                             | `2000m`          |
| `platform.resources.requests.memory`              | Memory resource requests                                                                                                                          | `4Gi`            |


### Dependencies

Enable and configure chart dependencies if not available in your deployment

| Name                                | Description                                                                                          | Value                       |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------- | --------------------------- |
| `postgresql.enabled`                | Switch to enable or disable the PostgreSQL helm chart                                                | `true`                      |
| `postgresql.auth.username`          | Name for a custom user to create                                                                     | `conduktor`                 |
| `postgresql.auth.password`          | Password for the custom user to create                                                               | `conduktorpassword`         |
| `postgresql.auth.postgresPassword`  | Password for the "postgres" admin user.                                                              | `""`                        |
| `postgresql.auth.database`          | Name for a custom database to create                                                                 | `conduktor_platform`        |
| `postgresql.primary.extraEnvVarsCM` | Name of existing ConfigMap containing extra env vars for PostgreSQL Primary nodes                    | `postgresql-extra-env-vars` |
| `minio.enabled`                     | Switch to enable or disable the Minio helm chart                                                     | `true`                      |
| `minio.mode`                        | Minio mode (standalone or distributed)                                                               | `standalone`                |
| `minio.disableWebUI`                | Toggle Minio Console                                                                                 | `true`                      |
| `minio.defaultBuckets`              | Default buckets to create                                                                            | `conduktor-monitoring`      |
| `minio.auth.rootUser`               | Root access key                                                                                      | `""`                        |
| `minio.auth.rootPassword`           | Root secret key                                                                                      | `""`                        |
| `minio.auth.existingSecret`         | Name of existing secret containing minio credentials (must contain root-user and root-password keys) | `""`                        |
| `minio.persistence.enabled`         | Enable Minio persistence                                                                             | `true`                      |
| `minio.persistence.size`            | Size of Minio volume                                                                                 | `8Gi`                       |
| `kafka.enabled`                     | Deploy a kafka alongside platform-controller (This should only be used for testing purpose)          | `false`                     |


## Remove

```console
$ helm delete -n conduktor platform
```

## Platform configuration

- [Docker image environment vairables](https://docs.conduktor.io/platform/configuration/env-variables#docker-image-environment-variables)
- [Platform properties reference](https://docs.conduktor.io/platform/configuration/env-variables#platform-properties-reference)

## Generate doc

Install [readme-generator-for-helm](https://github.com/bitnami-labs/readme-generator-for-helm)

```console
readme-generator --readme README.md -v values.yaml
```

## Guides

### How to configure TLS for the platform

This guide will help you to deploy Conduktor Platform with TLS enabled, using your own certificates. It can be achieved
with two methods:

**Give your certificate to the chart**

1. Update `platform.config.tls.enabled` value to `true`
2. Update `platform.config.tls.cert` value with your raw certificate
3. Update `platform.config.tls.key` value with your raw certificate key

**Use of a custom TLS secret**:

1. Create a secret with your certificates ([how-to](https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets))
2. Update the `platform.config.tls.enabled` value to `true`
3. Update the `platform.config.tls.existingSecret` value to the name of your secret (must have keys: tls.crt, tls.key)
4. Deploy the chart

> **Note**: Depending on your ingress controller, you may need to add additional annotations to your ingress
> (e.g [nginx](https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/tls.md#ssl-passthrough)).

## Metrics

If you deployed [Prometheus operator](https://github.com/prometheus-operator/prometheus-operator), this chart optionally can create a Prometheus service monitor.

```yaml
controller:
  metrics:
    prometheus:
      serviceMonitor:
        enabled: false
```

Also, you could use the pod annotation.

```yaml
controller:
  podAnnotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/metrics"
```

## FAQ

- [Does the platform-controller is like a Kubernetes operator?](#does-the-platform-controller-is-like-a-kubernetes-operator)

### Does the platform-controller is like a Kubernetes operator?

yes this is similar to an operator but we don't define Custom Resource Definition (CRD) we follow the [controller pattern](https://kubernetes.io/docs/concepts/architecture/controller/)

## Need Help!

If you have any questions, please reach out to us on [Discord](https://discord.gg/gzTrmjdXdA)
