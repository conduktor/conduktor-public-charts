<a name="readme-top" id="readme-top"></a>
# Conduktor Platform

> If you have any questions or [feedback](https://product.conduktor.help/c/55-helm-chart) contact our [support](https://www.conduktor.io/contact/support/).

## TL;DR

```console
$ helm repo add conduktor https://helm.conduktor.io
$ helm install my-platform conduktor/console \
    --create-namespace -n conduktor \
    --set config.organization.name="my-org" \
    --set config.admin.email="admin@conduktor.io" \
    --set config.admin.password="admin" \
    --set config.database.password="postgres" \
    --set config.database.username="postgres" \
    --set config.database.host="postgresql" \
    --set config.database.name="postgres" \
    --set config.license="${LICENSE}"
```

## Introduction

Helm Chart to deploy Conduktor Platform on Kubernetes.

[Snippets](#snippets) are available in this README to help you get started.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+

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

You can paste here your Conduktor Platform Configuration

Refer to our [documentation](https://docs.conduktor.io/platform/configuration/env-variables/) for the full list of product configuration properties.

| Name                                   | Description                                                                                                                                            | Value                          |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------ |
| `config.organization.name`             | Your Conduktor Platform Organization, you can only set it at install! You will need to change it in the Conduktor Platform UI after the installation   | `""`                           |
| `config.admin.email`                   | Your Conduktor Platform Admin email, you can only set it at install! You will need to change it in the Conduktor Platform UI after the installation    | `""`                           |
| `config.admin.password`                | Your Conduktor Platform Admin password, you can only set it at install! You will need to change it in the Conduktor Platform UI after the installation | `""`                           |
| `config.database.host`                 | Your Conduktor Platform Database host                                                                                                                  | `""`                           |
| `config.database.port`                 | Your Conduktor Platform Database port                                                                                                                  | `5432`                         |
| `config.database.name`                 | Your Conduktor Platform Database name                                                                                                                  | `postgres`                     |
| `config.database.username`             | Your Conduktor Platform Database username                                                                                                              | `""`                           |
| `config.database.password`             | Your Conduktor Platform Database password                                                                                                              | `""`                           |
| `config.license`                       | Conduktor Platform Enterprise license, if none given, the product will run in free tier                                                                | `""`                           |
| `config.existingLicenseSecret`         | Name of an existing secret containing the license                                                                                                      | `""`                           |
| `config.platform.external.url`         | Force the platform to redirect and use this URL (useful when behind a proxy to fix SSO issues)                                                         | `https://platform.example.com` |
| `config.platform.https.selfSigned`     | Enable HTTPS with a self-signed certificate (not recommended for production) based on 'config.platform.external.url' (required).                       | `false`                        |
| `config.platform.https.existingSecret` | Enable HTTPS with an existing secret containing the tls.crt and tls.key (required).                                                                    | `""`                           |

### Platform Deployment Parameters

| Name                                          | Description                                                                                                                                                   | Value                          |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| `platform.image.registry`                     | Conduktor Platform image registry                                                                                                                             | `docker.io`                    |
| `platform.image.repository`                   | Conduktor Platform image repository                                                                                                                           | `conduktor/conduktor-platform` |
| `platform.image.tag`                          | Conduktor Platform image tag (immutable tags are recommended)                                                                                                 | `1.17.3`                       |
| `platform.image.digest`                       | Conduktor Platform image digest in the way sha256:aa.... Please note this parameter, if set, will override the tag image tag (immutable tags are recommended) | `""`                           |
| `platform.image.pullPolicy`                   | Conduktor Platform image pull policy                                                                                                                          | `IfNotPresent`                 |
| `platform.image.pullSecrets`                  | Conduktor Platform image pull secrets                                                                                                                         | `[]`                           |
| `platform.image.debug`                        | Enable Conduktor Platform image debug mode                                                                                                                    | `false`                        |
| `platform.replicaCount`                       | Number of Conduktor Platform replicas to deploy                                                                                                               | `1`                            |
| `platform.containerPorts.http`                | Conduktor Platform HTTP (or HTTPS if configured) container port                                                                                               | `8080`                         |
| `platform.livenessProbe.enabled`              | Enable livenessProbe on Conduktor Platform containers                                                                                                         | `true`                         |
| `platform.livenessProbe.initialDelaySeconds`  | Initial delay seconds for livenessProbe                                                                                                                       | `60`                           |
| `platform.livenessProbe.periodSeconds`        | Period seconds for livenessProbe                                                                                                                              | `10`                           |
| `platform.livenessProbe.timeoutSeconds`       | Timeout seconds for livenessProbe                                                                                                                             | `5`                            |
| `platform.livenessProbe.failureThreshold`     | Failure threshold for livenessProbe                                                                                                                           | `3`                            |
| `platform.livenessProbe.successThreshold`     | Success threshold for livenessProbe                                                                                                                           | `1`                            |
| `platform.readinessProbe.enabled`             | Enable readinessProbe on Conduktor Platform containers                                                                                                        | `true`                         |
| `platform.readinessProbe.initialDelaySeconds` | Initial delay seconds for readinessProbe                                                                                                                      | `60`                           |
| `platform.readinessProbe.periodSeconds`       | Period seconds for readinessProbe                                                                                                                             | `10`                           |
| `platform.readinessProbe.timeoutSeconds`      | Timeout seconds for readinessProbe                                                                                                                            | `5`                            |
| `platform.readinessProbe.failureThreshold`    | Failure threshold for readinessProbe                                                                                                                          | `3`                            |
| `platform.readinessProbe.successThreshold`    | Success threshold for readinessProbe                                                                                                                          | `1`                            |
| `platform.startupProbe.enabled`               | Enable startupProbe on Conduktor Platform containers                                                                                                          | `true`                         |
| `platform.startupProbe.initialDelaySeconds`   | Initial delay seconds for startupProbe                                                                                                                        | `10`                           |
| `platform.startupProbe.periodSeconds`         | Period seconds for startupProbe                                                                                                                               | `10`                           |
| `platform.startupProbe.timeoutSeconds`        | Timeout seconds for startupProbe                                                                                                                              | `5`                            |
| `platform.startupProbe.failureThreshold`      | Failure threshold for startupProbe                                                                                                                            | `10`                           |
| `platform.startupProbe.successThreshold`      | Success threshold for startupProbe                                                                                                                            | `1`                            |
| `platform.customLivenessProbe`                | Custom livenessProbe that overrides the default one                                                                                                           | `{}`                           |
| `platform.customReadinessProbe`               | Custom readinessProbe that overrides the default one                                                                                                          | `{}`                           |
| `platform.customStartupProbe`                 | Custom startupProbe that overrides the default one                                                                                                            | `{}`                           |
| `platform.resources.limits.cpu`               | CPU limit for the platform container                                                                                                                          | `4000m`                        |
| `platform.resources.limits.memory`            | Memory limit for the container                                                                                                                                | `8Gi`                          |
| `platform.resources.requests.cpu`             | CPU resource requests                                                                                                                                         | `2000m`                        |
| `platform.resources.requests.memory`          | Memory resource requests                                                                                                                                      | `4Gi`                          |
| `platform.podSecurityContext`                 | Conduktor Platform Pod Security Context                                                                                                                       | `{}`                           |
| `platform.containerSecurityContext`           | Conduktor Platform containers' Security Context                                                                                                               | `{}`                           |
| `platform.existingConfigmap`                  | The name of an existing ConfigMap with your custom configuration for Conduktor Platform                                                                       | `""`                           |
| `platform.command`                            | Override default container command (useful when using custom images)                                                                                          | `[]`                           |
| `platform.args`                               | Override default container args (useful when using custom images)                                                                                             | `[]`                           |
| `platform.hostAliases`                        | Conduktor Platform pods host aliases                                                                                                                          | `[]`                           |
| `platform.podLabels`                          | Extra labels for Conduktor Platform pods                                                                                                                      | `{}`                           |
| `platform.podAnnotations`                     | Annotations for Conduktor Platform pods                                                                                                                       | `{}`                           |
| `platform.podAffinityPreset`                  | Pod affinity preset. Ignored if `platform.affinity` is set. Allowed values: `soft` or `hard`                                                                  | `""`                           |
| `platform.podAntiAffinityPreset`              | Pod anti-affinity preset. Ignored if `platform.affinity` is set. Allowed values: `soft` or `hard`                                                             | `soft`                         |
| `platform.nodeAffinityPreset.type`            | Node affinity preset type. Ignored if `platform.affinity` is set. Allowed values: `soft` or `hard`                                                            | `""`                           |
| `platform.nodeAffinityPreset.key`             | Node label key to match. Ignored if `platform.affinity` is set                                                                                                | `""`                           |
| `platform.nodeAffinityPreset.values`          | Node label values to match. Ignored if `platform.affinity` is set                                                                                             | `[]`                           |
| `platform.affinity`                           | Affinity for Conduktor Platform pods assignment                                                                                                               | `{}`                           |
| `platform.nodeSelector`                       | Node labels for Conduktor Platform pods assignment                                                                                                            | `{}`                           |
| `platform.tolerations`                        | Tolerations for Conduktor Platform pods assignment                                                                                                            | `[]`                           |
| `platform.updateStrategy.type`                | Conduktor Platform statefulset strategy type                                                                                                                  | `RollingUpdate`                |
| `platform.priorityClassName`                  | Conduktor Platform pods' priorityClassName                                                                                                                    | `""`                           |
| `platform.topologySpreadConstraints`          | Topology Spread Constraints for pod assignment spread across your cluster among failure-domains. Evaluated as a template                                      | `[]`                           |
| `platform.schedulerName`                      | Name of the k8s scheduler (other than default) for Conduktor Platform pods                                                                                    | `""`                           |
| `platform.terminationGracePeriodSeconds`      | Seconds Redmine pod needs to terminate gracefully                                                                                                             | `""`                           |
| `platform.lifecycleHooks`                     | for the Conduktor Platform container(s) to automate configuration before or after startup                                                                     | `{}`                           |
| `platform.extraEnvVars`                       | Array with extra environment variables to add to Conduktor Platform nodes                                                                                     | `[]`                           |
| `platform.extraEnvVarsCM`                     | Name of existing ConfigMap containing extra env vars for Conduktor Platform nodes                                                                             | `""`                           |
| `platform.extraEnvVarsSecret`                 | Name of existing Secret containing extra env vars for Conduktor Platform nodes                                                                                | `""`                           |
| `platform.extraVolumes`                       | Optionally specify extra list of additional volumes for the Conduktor Platform pod(s)                                                                         | `[]`                           |
| `platform.extraVolumeMounts`                  | Optionally specify extra list of additional volumeMounts for the Conduktor Platform container(s)                                                              | `[]`                           |
| `platform.sidecars`                           | Add additional sidecar containers to the Conduktor Platform pod(s)                                                                                            | `[]`                           |
| `platform.initContainers`                     | Add additional init containers to the Conduktor Platform pod(s)                                                                                               | `[]`                           |

### Traffic Exposure Parameters

| Name                               | Description                                                                                                                      | Value                    |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| `service.type`                     | Conduktor Platform service type                                                                                                  | `ClusterIP`              |
| `service.ports.http`               | Conduktor Platform service HTTP port                                                                                             | `80`                     |
| `service.nodePorts.http`           | Node port for HTTP                                                                                                               | `""`                     |
| `service.clusterIP`                | Conduktor Platform service Cluster IP                                                                                            | `""`                     |
| `service.loadBalancerSourceRanges` | Conduktor Platform service Load Balancer sources                                                                                 | `[]`                     |
| `service.externalTrafficPolicy`    | Conduktor Platform service external traffic policy                                                                               | `Cluster`                |
| `service.annotations`              | Additional custom annotations for Conduktor Platform service                                                                     | `{}`                     |
| `service.extraPorts`               | Extra ports to expose in Conduktor Platform service (normally used with the `sidecars` value)                                    | `[]`                     |
| `service.sessionAffinity`          | Control where client requests go, to the same pod or round-robin                                                                 | `None`                   |
| `service.sessionAffinityConfig`    | Additional settings for the sessionAffinity                                                                                      | `{}`                     |
| `ingress.enabled`                  | Enable ingress record generation for Conduktor Platform                                                                          | `false`                  |
| `ingress.pathType`                 | Ingress path type                                                                                                                | `ImplementationSpecific` |
| `ingress.apiVersion`               | Force Ingress API version (automatically detected if not set)                                                                    | `""`                     |
| `ingress.hostname`                 | Default host for the ingress record                                                                                              | `platform.local`         |
| `ingress.ingressClassName`         | IngressClass that will be be used to implement the Ingress (Kubernetes 1.18+)                                                    | `""`                     |
| `ingress.path`                     | Default path for the ingress record                                                                                              | `/`                      |
| `ingress.annotations`              | Additional annotations for the Ingress resource. To enable certificate autogeneration, place here your cert-manager annotations. | `{}`                     |
| `ingress.tls`                      | Enable TLS configuration for the host defined at `ingress.hostname` parameter                                                    | `false`                  |
| `ingress.selfSigned`               | Create a TLS secret for this ingress record using self-signed certificates generated by Helm                                     | `false`                  |
| `ingress.extraHosts`               | An array with additional hostname(s) to be covered with the ingress record                                                       | `[]`                     |
| `ingress.extraPaths`               | An array with additional arbitrary paths that may need to be added to the ingress under the main host                            | `[]`                     |
| `ingress.extraTls`                 | TLS configuration for additional hostname(s) to be covered with this ingress record                                              | `[]`                     |
| `ingress.secrets`                  | Custom TLS certificates as secrets                                                                                               | `[]`                     |
| `ingress.extraRules`               | Additional rules to be covered with this ingress record                                                                          | `[]`                     |

### Other Parameters

| Name                                          | Description                                                      | Value   |
| --------------------------------------------- | ---------------------------------------------------------------- | ------- |
| `serviceAccount.create`                       | Specifies whether a ServiceAccount should be created             | `true`  |
| `serviceAccount.name`                         | The name of the ServiceAccount to use.                           | `""`    |
| `serviceAccount.annotations`                  | Additional Service Account annotations (evaluated as a template) | `{}`    |
| `serviceAccount.automountServiceAccountToken` | Automount service account token for the server service account   | `true`  |
| `test`                                        | Enable additional manifests for testing purposes                 | `false` |

## Snippets

### Console configuration 

If you are looking for additional snippets related to the configuration of 
console, we recommend you to look at our 
[documentation](https://docs.conduktor.io/platform/configuration/configuration-snippets/).

- [Install with a basic SSO configuration](#install-with-a-basic-sso-configuration)
- [Install with a registered kafka cluster](#install-with-a-kafka-cluster)
- [Install with an enterprise license](#install-with-an-enterprise-license)

### Kubernetes configuration 

- [Install with a PodAffinity](#install-with-a-podaffinity)
- [Install with a PodAntiAffinity](#install-with-a-podantiaffinity)
- [Install with a Toleration](#install-with-a-toleration)
- [Install with a Self-Signed Certificate](#install-with-self-signed-tls-certificate)
- [Install with a custom service account](#install-with-a-custom-service-account)
- [Install with a AWS EKS IAM Role](#install-with-a-aws-eks-iam-role)

- [Provide the license as a Kubernetes Secret](#provide-the-license-as-a-kubernetes-secret)
- [Provide the license as a Kubernetes ConfigMap](#provide-the-platform-config-as-a-kubernetes-configmap)

### Install with an enterprise license

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "admin@my-org.com"
    password: "admin"

  database:
    host: ''
    port: 5432
    name: 'postgres'
    username: ''
    password: ''

  license: "${ENTERPRISE_LICENSE}"
```    

### Install with a basic SSO configuration

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "admin@my-org.com"
    password: "admin"

  database:
    host: ''
    port: 5432
    name: 'postgres'
    username: ''
    password: ''
  sso:
    oauth2:
      - name: 'auth0'
        default: true
        client-id: <client_id>
        client-secret: <client_secret>
        callback-uri: http://localhost/auth/oauth/callback/auth0
        openid:
          issuer: https://conduktor-staging.eu.auth0.com/
  
  license: '<license_key>'
```

### Install with a kafka cluster

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "admin@my-org.com"
    password: "admin"

  database:
    host: ''
    port: 5432
    name: 'postgres'
    username: ''
    password: ''
  clusters:
    - id: my-local-kafka-cluster
      name: My Local Kafka Cluster
      color: '#0013E7'
      bootstrapServers: 'my-bootstrap-server:9092'
      schemaRegistry:
        id: my-schema-registry
        url: 'http://my-schema-registry:8081'
```

### Provide the license as a Kubernetes Secret

We expect the secret to contain a key named `license` which contains your
license key.

```shell
# values.yaml
config:
  organization:
    name: "<your_org_name>"

  admin:
    email: "<your_admin_email>"
    password: "<your_admin_password>"
    
  database:
    host: '<postgres_host>'
    port: 5432
    name: '<postgres_database>'
    username: '<postgres_username>'
    password: '<postgres_password>'

  existingLicenseSecret: "<your_secret_name>"
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
    host: ''
    port: 5432
    name: 'postgres'
    username: ''
    password: ''

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
    host: ''
    port: 5432
    name: 'postgres'
    username: ''
    password: ''

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
```

### Install with Self-Signed TLS certificate

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "admin@my-org.com"
    password: "admin"

  database:
    host: ''
    port: 5432
    name: 'postgres'
    username: ''
    password: ''

  platform:
    external:
      url: "https://platform.local"
    https:
      selfSigned: true
```

### Install with a custom TLS certificate on the platform Pod

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "admin@my-org.com"
    password: "admin"

  database:
    host: ''
    port: 5432
    name: 'postgres'
    username: ''
    password: ''

  platform:
    external:
      url: "https://platform.local"
    https:
      selfSigned: false
      existingSecret: "platform-tls"
ingress:
  secrets:
    - name: platform-tls
      certificate: |-
        -----BEGIN CERTIFICATE-----
        ...
        -----END CERTIFICATE-----
      key: |-
        -----BEGIN PRIVATE KEY-----
        ...
        -----END PRIVATE KEY-----
```

### Install with a custom service account

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "admin@my-org.com"
    password: "admin"

  database:
    host: ''
    port: 5432
    name: 'postgres'
    username: ''
    password: ''

serviceAccount:
  create: false
  name: "my-service-account"
```

### Install with a AWS EKS IAM Role

```yaml
config:
  organization:
    name: "my-org"

  admin:
    email: "admin@my-org.com"
    password: "admin"

  database:
    host: ''
    port: 5432
    name: 'postgres'
    username: ''
    password: ''

serviceAccount:
    annotations:
        eks.amazonaws.com/role-arn: "arn:aws:iam::123456789012:role/my-role"
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Troubleshooting

For guides and advanced help, please refer to our
[documentation](https://docs.conduktor.io/platform/installation/get-started/kubernetes),
or to our charts `README`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
