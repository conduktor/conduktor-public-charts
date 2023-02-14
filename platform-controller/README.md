# Platform-controller

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
$ helm install -n conduktor --create-namespace platform conduktor/platform
```

### With enterprise license

```console
$ helm install -n conduktor --create-namespace platform conduktor/platform \
   --set platform.config.license=YOUR_LICENSE \
   --set platform.config.organization=YOUR_ORGANIZATION \
   --set platform.config.adminEmail=admin@yourdomain.com \
   --set platform.config.adminPassword=TOP_SECRET
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
| `controller.image.tag`                 | Platform Controller image tag                                                | `0.5.0`                         |
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


### Platform parameters

Conduktor Platform parameters

| Name                                             | Description                                                     | Value                   |
| ------------------------------------------------ | --------------------------------------------------------------- | ----------------------- |
| `platform.commonLabels`                          | Common labels to add to all resources                           | `{}`                    |
| `platform.config.replicas`                       | Number of replicas for the platform controller                  | `1`                     |
| `platform.config.name`                           | Name of the platform controller                                 | `platform`              |
| `platform.config.organization`                   | Your organizations name                                         | `conduktor`             |
| `platform.config.adminEmail`                     | Email of the admin user                                         | `admin@conduktor.io`    |
| `platform.config.adminPassword`                  | Password of the admin user                                      | `admin`                 |
| `platform.config.modules.console`                | Enable or disable the console module                            | `true`                  |
| `platform.config.modules.data_masking`           | Enable or disable the data masking module                       | `true`                  |
| `platform.config.modules.monitoring`             | Enable or disable the monitoring module                         | `true`                  |
| `platform.config.modules.testing`                | Enable or disable the testing module                            | `true`                  |
| `platform.config.modules.topic_as_a_service`     | Enable or disable the topic as a service module                 | `true`                  |
| `platform.config.modules.governance`             | Enable or disable the governance module                         | `true`                  |
| `platform.config.monitoring`                     | External monitoring S3 storage                                  | `{}`                    |
| `platform.config.sso.enabled`                    | Enable or disable the SSO (only on enterprise plan)             | `false`                 |
| `platform.config.sso.ignoreUntrustedCertificate` | Disable SSL checks                                              | `false`                 |
| `platform.config.sso.ldap[0].name`               | LDAP connection name                                            | `""`                    |
| `platform.config.sso.ldap[0].server`             | LDAP server host and port                                       | `""`                    |
| `platform.config.sso.ldap[0].managerDn`          | Sets the manager DN                                             | `""`                    |
| `platform.config.sso.ldap[0].managerPassword`    | Sets the manager password                                       | `""`                    |
| `platform.config.sso.ldap[0].searchBase`         | Sets the base DN to search                                      | `""`                    |
| `platform.config.sso.ldap[0].groupsBase`         | Sets the base DN to search from                                 | `""`                    |
| `platform.config.sso.oauth2[0].name`             | OAuth2 connection name                                          | `""`                    |
| `platform.config.sso.oauth2[0].default`          | Use as default                                                  | `true`                  |
| `platform.config.sso.oauth2[0].clientId`         | OAuth2 client id                                                | `""`                    |
| `platform.config.sso.oauth2[0].clientSecret`     | OAuth2 client secret                                            | `""`                    |
| `platform.config.sso.oauth2[0].openid.issuer`    | Issuer to check on token                                        | `""`                    |
| `platform.config.license`                        | Enterprise license key. If not provided, fallback to free plan. | `""`                    |
| `platform.config.database.host`                  | Database host                                                   | `postgresql.postgresql` |
| `platform.config.database.port`                  | Database port                                                   | `5432`                  |
| `platform.config.database.username`              | Database user                                                   | `postgres`              |
| `platform.config.database.password`              | Database password, can be a string or can reference a secret.   | `conduktor`             |
| `platform.config.database.name`                  | Database name                                                   | `postgres`              |
| `platform.ingress.ingressClassName`              | Ingress class name for the platform                             | `""`                    |
| `platform.ingress.host`                          | Plaform host                                                    | `platform.local`        |
| `platform.ingress.tls.enabled`                   | Enable Platform TLS                                             | `false`                 |
| `platform.ingress.tls.host`                      | Platform Host                                                   | `nil`                   |
| `platform.ingress.tls.secretRef`                 | Secret name with keystore to load                               | `""`                    |
| `platform.ingress.annotations`                   | Additional annotations for the ingress                          | `{}`                    |
| `platform.resources.limits.cpu`                  | CPU limit for the platform container                            | `4000m`                 |
| `platform.resources.limits.memory`               | Memory limit for the container                                  | `8Gi`                   |
| `platform.resources.requests.cpu`                | CPU resource requests                                           | `2000m`                 |
| `platform.resources.requests.memory`             | Memory resource requests                                        | `4Gi`                   |


### Dependencies

Enable and configure chart dependencies if not available in your deployment

| Name                                | Description                                                                               | Value                       |
| ----------------------------------- | ----------------------------------------------------------------------------------------- | --------------------------- |
| `postgresql.enabled`                | Switch to enable or disable the PostgreSQL helm chart                                     | `true`                      |
| `postgresql.auth.username`          | Name for a custom user to create                                                          | `conduktor`                 |
| `postgresql.auth.password`          | Password for the custom user to create                                                    | `conduktorpassword`         |
| `postgresql.auth.postgresPassword`  | Password for the "postgres" admin user.                                                   | `""`                        |
| `postgresql.auth.database`          | Name for a custom database to create                                                      | `conduktor_platform`        |
| `postgresql.primary.extraEnvVarsCM` | Name of existing ConfigMap containing extra env vars for PostgreSQL Primary nodes         | `postgresql-extra-env-vars` |
| `kafka.enabled`                     | Deploy a kafka along side platform-controller (This should only used for testing purpose) | `false`                     |


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
