# Platform-controller

> **Warning**
> This chart is in **BETA** phase and is subject to change.
> The API may change without notice.
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
$ helm install -n conduktor --create-namespace platform conduktor/platform-controller
```

### With enterprise license

```console
$ helm install -n conduktor --create-namespace platform conduktor/platform-controller \
   --set platform.config.license=YOUR_LICENSE \
   --set platform.config.organization=YOUR_ORGANIZATION \
   --set platform.config.adminEmail=admin@yourdomain.com \
   --set platform.config.adminPassword=TOP_SECRET
```

## Versions matrix

| Conduktor Platform | Platform-controller | Helm chart |
|--------------------|---------------------|------------|
| 1.11.1             | 0.4.0               | 0.2.1      |
| 1.11.1             | 0.5.0               | 0.2.2      |
| 1.11.1             | 0.5.0               | 0.2.3      |
| 1.11.1             | 0.6.0               | 0.2.4      |
| 1.12.1             | 0.7.0               | 0.2.5      |

## Architecture
This Helm chart will deploy the Platform-controller that is responsible to deploy the Conduktor Platform on the same namespace.

Optionally it can deploy a Postgresql and/or a Kafka cluster inside the same namespace for demo purpose.

```
                          conduktor (namespace)
                        +--------------------------------------------------------------------------------------+
+------------+          |                                                                                      |
|            |          |          +-----------------------+                          +---------+              |
| Helm chart |  Deploy  |          |                       | Deploy        +----------> Ingress |              |
|            +--+-------+---------->  platform-controller  |               |          +----+----+              |
+------------+  |       |          |                       +---------------+               |                   |
                |       |          +-------+----------+----+               |               |                   |
                |       |                  |          |                    |         +-----v-----+             |
                |       |                  |  Watch   |                    +--------->  Service  |             |
                |       |                  |          |                    |         +-----+-----+             |
                |       |                  |          |                    |               |                   |
                |       |            +-----v-----+ +--v------+             |               |                   |
                |       |            |           | |         |             |     +---------v--------------+    |
                |       |            | ConfigMap | | Secret  |             |     |                        |    |
                |       |            |           | |         |             +----->   conduktor-platform   |    |
                |       |            +------^----+ +---^-----+                   |                        |    |
                |       |                   |          |                         +--------+---------------+    |
                |       |                   |          |                                  |                    |
                +-------+-----------+-------+----------+-+                                |Connect to          |
                        |           |                    |                                |                    |
                        |        +--v----------+     +---v----------+                     |                    |
                        |        |             |     |              |                     |                    |
                        |        | Postgresql  |     |  Kafka       |                     |                    |
                        |        |  (optional) |     |   (optional) |                     |                    |
                        |        |             |     |              |                     |                    |
                        |        +------^------+     +--------^-----+                     |                    |
                        |               |                     |                           |                    |
                        |               +---------------------+---------------------------+                    |
                        |                                                                                      |
                        +--------------------------------------------------------------------------------------+
```

## Parameters

### Global parameters

| Name                      | Description                              | Value |
| ------------------------- | ---------------------------------------- | ----- |
| `global.imageRegistry`    | Global Docker image registry             | `""`  |
| `global.imagePullSecrets` | Docker login secrets name for image pull | `[]`  |


### Controller parameters

Conduktor Controller parameters

| Name                                   | Description                                                                  | Value                           |
| -------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------- |
| `controller.image.registry`            | Platform Controller image registry                                           | `docker.io`                     |
| `controller.image.repository`          | Platform Controller image repository                                         | `conduktor/platform-controller` |
| `controller.image.pullPolicy`          | Platform Controller image pull policy                                        | `Always`                        |
| `controller.image.tag`                 | Platform Controller image tag                                                | `0.7.0`                         |
| `controller.commonLabels`              | Common labels to add to all resources                                        | `{}`                            |
| `controller.commonAnnotations`         | Common annotations to add to all resources                                   | `{}`                            |
| `controller.serviceAccount.create`     | Create Kubernetes service account.                                           | `true`                          |
| `controller.serviceAccount.name`       | Service account name override                                                | `conduktor-controller`          |
| `controller.resources.limits.cpu`      | CPU limit for the platform controller                                        | `100m`                          |
| `controller.resources.limits.memory`   | Memory limit for the platform controller                                     | `128Mi`                         |
| `controller.resources.requests.cpu`    | CPU resource requests for platform controller                                | `100m`                          |
| `controller.resources.requests.memory` | Memory resource requests for platform controller                             | `128Mi`                         |
| `controller.ingress.ingressClassName`  | Ingress class name for the controller                                        | `""`                            |
| `controller.ingress.host`              | Platform controller Host                                                     | `controller.private`            |
| `controller.ingress.extraHosts`        | An array with additional hostname(s) to be covered with this ingress record. | `[]`                            |
| `controller.ingress.tls.enabled`       | Enable TLS for the controller ingress                                        | `false`                         |
| `controller.ingress.tls.host`          | Host                                                                         | `nil`                           |
| `controller.ingress.tls.secretRef`     | Secret name with keystore to load                                            | `""`                            |
| `controller.ingress.annotations`       | Additional annotations for the ingress                                       | `{}`                            |
| `controller.service.annotations`       | Annotations for controller service                                           | `{}`                            |
| `controller.service.http.port`         | HTTP port                                                                    | `8080`                          |
| `controller.extraEnvVars`              | Array with extra environment variables                                       | `[]`                            |
| `controller.extraEnvVarsCM`            | Name of existing ConfigMap containing extra env vars                         | `""`                            |
| `controller.extraEnvVarsSecret`        | Name of existing Secret containing extra env vars                            | `""`                            |


### Platform parameters

Conduktor Platform parameters

| Name                                              | Description                                                     | Value                   |
| ------------------------------------------------- | --------------------------------------------------------------- | ----------------------- |
| `platform.commonLabels`                           | Common labels to add to all resources                           | `{}`                    |
| `platform.existingSecret`                         | Existing secret for platform                                    | `""`                    |
| `platform.config.replicas`                        | Number of replicas for the platform controller                  | `1`                     |
| `platform.config.name`                            | Name of the platform controller                                 | `platform`              |
| `platform.config.organization`                    | Your organizations name                                         | `conduktor`             |
| `platform.config.adminEmail`                      | Email of the admin user                                         | `admin@conduktor.io`    |
| `platform.config.adminPassword`                   | Password of the admin user                                      | `admin`                 |
| `platform.config.modules.console`                 | Enable or disable the console module                            | `true`                  |
| `platform.config.modules.data_masking`            | Enable or disable the data masking module                       | `true`                  |
| `platform.config.modules.monitoring`              | Enable or disable the monitoring module                         | `true`                  |
| `platform.config.modules.testing`                 | Enable or disable the testing module                            | `true`                  |
| `platform.config.modules.topic_as_a_service`      | Enable or disable the topic as a service module                 | `true`                  |
| `platform.config.modules.governance`              | Enable or disable the governance module                         | `true`                  |
| `platform.config.monitoring.storage.s3.bucket`    | S3 bucket name                                                  | `""`                    |
| `platform.config.monitoring.storage.s3.endpoint`  | S3 endpoint                                                     | `""`                    |
| `platform.config.monitoring.storage.s3.accessKey` | S3 access key                                                   | `""`                    |
| `platform.config.monitoring.storage.s3.secretKey` | S3 secret key                                                   | `""`                    |
| `platform.config.monitoring.storage.s3.region`    | S3 region                                                       | `""`                    |
| `platform.config.monitoring.storage.s3.insecure`  | S3 insecure                                                     | `true`                  |
| `platform.config.sso.enabled`                     | Enable or disable the SSO (only on enterprise plan)             | `false`                 |
| `platform.config.sso.ignoreUntrustedCertificate`  | Disable SSL checks                                              | `false`                 |
| `platform.config.sso.ldap.name`                   | LDAP connection name                                            | `""`                    |
| `platform.config.sso.ldap.server`                 | LDAP server host and port                                       | `""`                    |
| `platform.config.sso.ldap.managerDn`              | Sets the manager DN                                             | `""`                    |
| `platform.config.sso.ldap.managerPassword`        | Sets the manager password                                       | `""`                    |
| `platform.config.sso.ldap.searchBase`             | Sets the base DN to search                                      | `""`                    |
| `platform.config.sso.ldap.groupsBase`             | Sets the base DN to search from                                 | `""`                    |
| `platform.config.sso.oauth2.name`                 | OAuth2 connection name                                          | `""`                    |
| `platform.config.sso.oauth2.default`              | Use as default                                                  | `true`                  |
| `platform.config.sso.oauth2.clientId`             | OAuth2 client id                                                | `""`                    |
| `platform.config.sso.oauth2.clientSecret`         | OAuth2 client secret                                            | `""`                    |
| `platform.config.sso.oauth2.openid.issuer`        | Issuer to check on token                                        | `""`                    |
| `platform.config.license`                         | Enterprise license key. If not provided, fallback to free plan. | `""`                    |
| `platform.config.database.host`                   | Database host                                                   | `postgresql.postgresql` |
| `platform.config.database.port`                   | Database port                                                   | `5432`                  |
| `platform.config.database.username`               | Database user                                                   | `postgres`              |
| `platform.config.database.password`               | Database password, can be a string or can reference a secret.   | `conduktor`             |
| `platform.config.database.name`                   | Database name                                                   | `postgres`              |
| `platform.extraEnvVars`                           | Array with extra environment variables                          | `[]`                    |
| `platform.extraEnvVarsCM`                         | Name of existing ConfigMap containing extra env vars            | `""`                    |
| `platform.extraEnvVarsSecret`                     | Name of existing Secret containing extra env vars               | `""`                    |
| `platform.ingress.ingressClassName`               | Ingress class name for the platform                             | `""`                    |
| `platform.ingress.host`                           | Plaform host                                                    | `platform.local`        |
| `platform.ingress.tls.enabled`                    | Enable Platform TLS                                             | `false`                 |
| `platform.ingress.tls.host`                       | Platform Host                                                   | `nil`                   |
| `platform.ingress.tls.secretRef`                  | Secret name with keystore to load                               | `""`                    |
| `platform.ingress.annotations`                    | Additional annotations for the ingress                          | `{}`                    |
| `platform.resources.limits.cpu`                   | CPU limit for the platform container                            | `4000m`                 |
| `platform.resources.limits.memory`                | Memory limit for the container                                  | `8Gi`                   |
| `platform.resources.requests.cpu`                 | CPU resource requests                                           | `2000m`                 |
| `platform.resources.requests.memory`              | Memory resource requests                                        | `4Gi`                   |


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
| `kafka.enabled`                     | Deploy a kafka along side platform-controller (This should only used for testing purpose)            | `false`                     |


## Remove

```console
$ helm delete -n conduktor platform
```

## Platform configuration

* [Docker image environment vairables](https://docs.conduktor.io/platform/configuration/env-variables#docker-image-environment-variables)
* [Platform properties reference](https://docs.conduktor.io/platform/configuration/env-variables#platform-properties-reference)

## Generate doc
Install [readme-generator-for-helm](https://github.com/bitnami-labs/readme-generator-for-helm)

```console
readme-generator --readme README.md -v values.yaml
```

## Need Help!

If you have any questions, please reach out to us on [Discord](https://discord.gg/gzTrmjdXdA)
