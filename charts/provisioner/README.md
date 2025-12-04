<a name="readme-top" id="readme-top"></a>

# Conduktor Provisioner

> If you have any questions you can [submit feedback](https://support.conduktor.io/hc/en-gb/requests/new?ticket_form_id=17438365654417) or contact [support](https://www.conduktor.io/contact/support/).

* [Introduction](#introduction)
* [Prerequisites](#prerequisites)
* [Usage](#usage)
* [Limitations](#limitations)
* [Parameters](#parameters)
  * [Global parameters](#global-parameters)
  * [Common parameters](#common-parameters)
  * [conduktor-ctl Parameters](#conduktor-ctl-parameters)
  * [Init wait-for script configuration](#init-wait-for-script-configuration)
  * [Conduktor Console provisioning configuration](#conduktor-console-provisioning-configuration)
  * [Conduktor Gateway provisioning configuration](#conduktor-gateway-provisioning-configuration)
  * [Other Parameters](#other-parameters)
* [Examples values](#examples-values)
  * [Provision Console](#provision-console)
  * [Provision Gateway](#provision-gateway)
  * [Provision Console and Gateway](#provision-console-and-gateway)
  * [Use secrets and configmaps for configuration](#use-secrets-and-configmaps-for-configuration)
  * [Provide manifests from a ConfigMap](#provide-manifests-from-a-configmap)
  * [Using different CLI commands](#using-different-cli-commands)
  * [Using CronJob to run the provisioner](#using-cronjob-to-run-the-provisioner)
* [Troubleshooting](#troubleshooting)

## Introduction

Helm Chart to deploy Conduktor Provisioner on Kubernetes that will provision existing Conduktor products.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+
- Conduktor Console 1.23.0+ (depending on the resources, check [documentation](https://docs.conduktor.io/platform/reference/resource-reference/) for more details)
- Conduktor Gateway 3.1.0+ (depending on the resources, check [documentation](https://docs.conduktor.io/gateway/reference/resources-reference/) for more details)

## Usage

```shell
# Add the Conduktor Helm repository
helm repo add conduktor https://helm.conduktor.io

# Install Conduktor Console
helm install platform conduktor/console \
    --create-namespace -n conduktor \
    --set config.admin.email="admin@conduktor.io" \
    --set config.admin.password="admin123!" \
    --set config.database.password="postgres" \
    --set config.database.username="postgres" \
    --set config.database.host="postgresql" \
    --set config.database.name="postgres" \
    --set config.license="${LICENSE}"

# Push Conduktor CLI compatible YAML manifests files into a ConfigMap. See https://github.com/conduktor/ctl
kubectl create configmap setup-manifests --from-file=./manifests/console-setup.yaml -n conduktor

# Use Provisioner chart to provision Console
helm install setup conduktor/provisioner \
    -n conduktor \
    --set console.enabled=true \
    --set console.url="http://console.conduktor" \
    --set console.username="admin@conduktor.io" \
    --set console.password="admin123!" \
    --set console.extraManifestsConfigMapRef[0].name="setup-manifests" \
    --set console.extraManifestsConfigMapRef[0].key="console-setup.yaml"
```

More examples can be found in the [Examples values](#examples-values) section.

## Limitations

As a job using Conduktor CLI, the provisioner **does not keep track of the resources** it creates.
So if you remove a resource from the manifests, it will **not be removed from target API**.
If you want to manage resources lifecycle, you should use [Conduktor Terraform provider](https://registry.terraform.io/providers/conduktor/conduktor/latest) instead.


## Parameters

### Global parameters

| Name                                                  | Description                                                                                                                                                                                                                                                                                                                                                         | Value   |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `global.imageRegistry`                                | Global Docker image registry                                                                                                                                                                                                                                                                                                                                        | `""`    |
| `global.imagePullSecrets`                             | Global Docker registry secret names as an array                                                                                                                                                                                                                                                                                                                     | `[]`    |
| `global.security.allowInsecureImages`                 | Allows skipping image verification                                                                                                                                                                                                                                                                                                                                  | `false` |
| `global.compatibility.openshift.adaptSecurityContext` | Adapt the securityContext sections of the deployment to make them compatible with Openshift restricted-v2 SCC: remove runAsUser, runAsGroup and fsGroup and let the platform use their allowed default IDs. Possible values: auto (apply if the detected running cluster is Openshift), force (perform the adaptation always), disabled (do not perform adaptation) | `auto`  |
| `global.compatibility.omitEmptySeLinuxOptions`        | If set to true, removes the seLinuxOptions from the securityContexts when it is set to an empty object                                                                                                                                                                                                                                                              | `false` |

### Common parameters

Configuration provisioning job and other common parameters.

| Name                     | Description                                                                             | Value           |
| ------------------------ | --------------------------------------------------------------------------------------- | --------------- |
| `nameOverride`           | String to partially override common.names.name                                          | `""`            |
| `fullnameOverride`       | String to fully override common.names.fullname                                          | `""`            |
| `namespaceOverride`      | String to fully override common.names.namespace                                         | `""`            |
| `commonLabels`           | Labels to add to all deployed objects                                                   | `{}`            |
| `commonAnnotations`      | Annotations to add to all deployed objects                                              | `{}`            |
| `useHooks`               | Enable Helm hooks for the conduktor-provisioner Job and CronJob                         | `true`          |
| `clusterDomain`          | Kubernetes cluster domain name                                                          | `cluster.local` |
| `extraDeploy`            | Array of extra objects to deploy with the release                                       | `[]`            |
| `diagnosticMode.enabled` | Enable diagnostic mode (all probes will be disabled and the command will be overridden) | `false`         |
| `diagnosticMode.command` | Command to override all containers in the chart release                                 | `["sleep"]`     |
| `diagnosticMode.args`    | Args to override all containers in the chart release                                    | `["infinity"]`  |

### conduktor-ctl Parameters

Configuration of the conduktor-ctl image used to run the Conduktor CLI commands.

| Name                                 | Description                                                                                                                                              | Value                     |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| `image.registry`                     | conduktor-ctl image registry                                                                                                                             | `docker.io`               |
| `image.repository`                   | conduktor-ctl image repository                                                                                                                           | `conduktor/conduktor-ctl` |
| `image.tag`                          | conduktor-ctl image tag (immutable tags are recommended)                                                                                                 | `v0.6.2`                  |
| `image.digest`                       | conduktor-ctl image digest in the way sha256:aa.... Please note this parameter, if set, will override the tag image tag (immutable tags are recommended) | `""`                      |
| `image.pullPolicy`                   | conduktor-ctl image pull policy                                                                                                                          | `IfNotPresent`            |
| `image.pullSecrets`                  | conduktor-ctl image pull secrets                                                                                                                         | `[]`                      |
| `image.debug`                        | Enable conduktor-ctl image debug mode                                                                                                                    | `false`                   |
| `cronJob.enabled`                    | Configure conduktor-provisioner job as a CronJob                                                                                                         | `false`                   |
| `cronJob.schedule`                   | Schedule for the CronJob, by default empty string (no schedule)                                                                                          | `""`                      |
| `cronJob.timezone`                   | Timezone for the CronJob, by default empty string (no timezone)                                                                                          | `""`                      |
| `cronJob.concurrencyPolicy`          | Concurrency policy for the CronJob, by default "Replace"                                                                                                 | `Replace`                 |
| `cronJob.suspend`                    | Suspend the CronJob, by default false (not suspended)                                                                                                    | `false`                   |
| `cronJob.successfulJobsHistoryLimit` | Number of successful jobs to keep in history                                                                                                             | `3`                       |
| `cronJob.failedJobsHistoryLimit`     | Number of failed jobs to keep in history                                                                                                                 | `1`                       |
| `cleanupAfterFinished.enabled`       | Enable cleanup of Job after it's finished                                                                                                                | `false`                   |
| `cleanupAfterFinished.seconds`       | TTL to cleanup the Job after it's finished                                                                                                               | `600`                     |
| `restartPolicy`                      | Restart policy for conduktor-provisioner jobs                                                                                                            | `OnFailure`               |
| `backoffLimit`                       | Number of retries before the job is considered failed                                                                                                    | `10`                      |
| `podSecurityContext`                 | conduktor-provisioner Pod Security Context                                                                                                               | `{}`                      |
| `podLabels`                          | Extra labels for conduktor-provisioner pods                                                                                                              | `{}`                      |
| `podAnnotations`                     | Annotations for conduktor-provisioner pods                                                                                                               | `{}`                      |
| `podAffinityPreset`                  | Pod affinity preset. Ignored if `affinity` is set. Allowed values: `soft` or `hard`                                                                      | `""`                      |
| `podAntiAffinityPreset`              | Pod anti-affinity preset. Ignored if `affinity` is set. Allowed values: `soft` or `hard`                                                                 | `soft`                    |
| `nodeAffinityPreset.type`            | Node affinity preset type. Ignored if `affinity` is set. Allowed values: `soft` or `hard`                                                                | `""`                      |
| `nodeAffinityPreset.key`             | Node label key to match. Ignored if `affinity` is set                                                                                                    | `""`                      |
| `nodeAffinityPreset.values`          | Node label values to match. Ignored if `affinity` is set                                                                                                 | `[]`                      |
| `priorityClassName`                  | conduktor-provisioner pods' priorityClassName                                                                                                            | `""`                      |
| `affinity`                           | Affinity for conduktor-provisioner pods assignment                                                                                                       | `{}`                      |
| `nodeSelector`                       | Node labels for conduktor-provisioner pods assignment                                                                                                    | `{}`                      |
| `tolerations`                        | Tolerations for conduktor-provisioner pods assignment                                                                                                    | `[]`                      |
| `schedulerName`                      | Name of the k8s scheduler (other than default) for conduktor-provisioner pods                                                                            | `""`                      |
| `terminationGracePeriodSeconds`      | Seconds conduktor-provisioner pods need to terminate gracefully                                                                                          | `""`                      |
| `topologySpreadConstraints`          | Topology Spread Constraints for conduktor-provisioner pod assignment spread across your cluster among failure-domains                                    | `[]`                      |
| `initContainers`                     | List of init containers to add to the conduktor-provisioner job pod                                                                                      | `[]`                      |

### Init wait-for script configuration

Configures the wait-for scripts and image used to wait for the services to be ready before running the provisioner jobs.

| Name                        | Description                                                                                                                                              | Value             |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| `waitFor.image.registry`    | registry for wait-for curl image                                                                                                                         | `docker.io`       |
| `waitFor.image.repository`  | wait-for curl image repository                                                                                                                           | `curlimages/curl` |
| `waitFor.image.tag`         | wait-for curl image tag (immutable tags are recommended)                                                                                                 | `8.15.0`          |
| `waitFor.image.digest`      | wait-for curl image digest in the way sha256:aa.... Please note this parameter, if set, will override the tag image tag (immutable tags are recommended) | `""`              |
| `waitFor.image.pullPolicy`  | wait-for image pull policy                                                                                                                               | `IfNotPresent`    |
| `waitFor.image.pullSecrets` | wait-for image pull secrets                                                                                                                              | `[]`              |
| `waitFor.retries`           | Number of retries to wait for the service to be ready                                                                                                    | `10`              |
| `waitFor.retryInterval`     | Interval in seconds between retries                                                                                                                      | `5`               |

### Conduktor Console provisioning configuration

Configuration of Conduktor Console provisioning container using Conduktor CLI.

| Name                                 | Description                                                                                                                  | Value                       |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| `console.enabled`                    | Enable Console provisioning                                                                                                  | `false`                     |
| `console.authMode`                   | Authentication mode on Console for Conduktor CLI, either "conduktor" or "external" if using API Gateway in front of Console. | `conduktor`                 |
| `console.url`                        | URL of the Console (mandatory)                                                                                               | `""`                        |
| `console.username`                   | Username to authenticate on the Console. Can be passed as an environment variable `CDK_USER`                                 | `""`                        |
| `console.password`                   | Password to authenticate on the Console. Can be passed as an environment variable `CDK_PASSWORD`                             | `""`                        |
| `console.apiToken`                   | API Token to authenticate on the Console. Can be passed as an environment variable `CDK_API_KEY`                             | `""`                        |
| `console.caCert`                     | CA certificate of Console. Can be passed as an environment variable `CDK_CACERT`                                             | `""`                        |
| `console.cert`                       | Authentication certificate to access Console. Can be passed as an environment variable `CDK_CERT`                            | `""`                        |
| `console.key`                        | Authentication certificate key to access Console. Can be passed as an environment variable `CDK_KEY`                         | `""`                        |
| `console.insecure`                   | Skip TLS verification                                                                                                        | `false`                     |
| `console.debug`                      | Enable verbose debug mode                                                                                                    | `true`                      |
| `console.manifests`                  | Manifests YAML to apply on the Console                                                                                       | `[]`                        |
| `console.manifestsConfigMap`         | Manifests YAML to apply on the Console                                                                                       | `""`                        |
| `console.manifestsConfigMapKey`      | Manifests YAML to apply on the Console                                                                                       | `00-console-resources.yaml` |
| `console.extraManifestsConfigMapRef` | List of ConfigMaps references with extra manifests to apply on the Console                                                   | `[]`                        |
| `console.command`                    | Override default conduktor-provisioner container command (useful when using custom images)                                   | `["/bin/conduktor"]`        |
| `console.args`                       | Override default conduktor-provisioner container args (useful when using custom images)                                      | `["apply","-f","/conf"]`    |
| `console.extraEnvVars`               | Array with extra environment variables to add to conduktor-provisioner containers                                            | `[]`                        |
| `console.extraEnvVarsCM`             | Name of existing ConfigMap containing extra env vars for conduktor-provisioner containers                                    | `""`                        |
| `console.extraEnvVarsSecret`         | Name of existing Secret containing extra env vars for conduktor-provisioner containers                                       | `""`                        |
| `console.extraVolumes`               | Optionally specify extra list of additional volumes for the conduktor-provisioner pods                                       | `[]`                        |
| `console.extraVolumeMounts`          | Optionally specify extra list of additional volumeMounts for the conduktor-provisioner containers                            | `[]`                        |
| `console.resources.requests.cpu`     | CPU resource requests                                                                                                        | `100m`                      |
| `console.resources.requests.memory`  | Memory resource requests                                                                                                     | `50Mi`                      |
| `console.resources.limits.cpu`       | CPU limit for the platform container                                                                                         | `500m`                      |
| `console.resources.limits.memory`    | Memory limit for the container                                                                                               | `128Mi`                     |
| `console.containerSecurityContext`   | conduktor-provisioner containers' Security Context                                                                           | `{}`                        |

### Conduktor Gateway provisioning configuration

Configuration of Conduktor Gateway provisioning container using Conduktor CLI.

| Name                                 | Description                                                                                                          | Value                       |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| `gateway.enabled`                    | Enable Gateway provisioning                                                                                          | `false`                     |
| `gateway.url`                        | URL of the Gateway (mandatory).                                                                                      | `""`                        |
| `gateway.username`                   | Username to authenticate on the Gateway (mandatory). Can be passed as an environment variable `CDK_GATEWAY_USER`     | `""`                        |
| `gateway.password`                   | Password to authenticate on the Gateway (mandatory). Can be passed as an environment variable `CDK_GATEWAY_PASSWORD` | `""`                        |
| `gateway.caCert`                     | CA certificate of Gateway. Can be passed as an environment variable `CDK_CACERT`                                     | `""`                        |
| `gateway.cert`                       | Authentication certificate to access Gateway. Can be passed as an environment variable `CDK_CERT`                    | `""`                        |
| `gateway.key`                        | Authentication certificate key to access Gateway. Can be passed as an environment variable `CDK_KEY`                 | `""`                        |
| `gateway.insecure`                   | Skip TLS verification                                                                                                | `false`                     |
| `gateway.debug`                      | Enable verbose debug mode                                                                                            | `true`                      |
| `gateway.manifests`                  | Manifests YAML to apply on the Gateway                                                                               | `[]`                        |
| `gateway.manifestsConfigMap`         | Manifests YAML to apply on the Gateway                                                                               | `""`                        |
| `gateway.manifestsConfigMapKey`      | Manifests YAML to apply on the Gateway                                                                               | `00-gateway-resources.yaml` |
| `gateway.extraManifestsConfigMapRef` | List of ConfigMaps references with extra manifests to apply on the Gateway                                           | `[]`                        |
| `gateway.command`                    | Override default conduktor-provisioner container command                                                             | `["/bin/conduktor"]`        |
| `gateway.args`                       | Override default conduktor-provisioner container args                                                                | `["apply","-f","/conf"]`    |
| `gateway.extraEnvVars`               | Array with extra environment variables to add to conduktor-provisioner containers                                    | `[]`                        |
| `gateway.extraEnvVarsCM`             | Name of existing ConfigMap containing extra env vars for conduktor-provisioner containers                            | `""`                        |
| `gateway.extraEnvVarsSecret`         | Name of existing Secret containing extra env vars for conduktor-provisioner containers                               | `""`                        |
| `gateway.extraVolumes`               | Optionally specify extra list of additional volumes for the conduktor-provisioner pods                               | `[]`                        |
| `gateway.extraVolumeMounts`          | Optionally specify extra list of additional volumeMounts for the conduktor-provisioner containers                    | `[]`                        |
| `gateway.resources.requests.cpu`     | CPU resource requests                                                                                                | `100m`                      |
| `gateway.resources.requests.memory`  | Memory resource requests                                                                                             | `50Mi`                      |
| `gateway.resources.limits.cpu`       | CPU limit for the platform container                                                                                 | `500m`                      |
| `gateway.resources.limits.memory`    | Memory limit for the container                                                                                       | `128Mi`                     |
| `gateway.containerSecurityContext`   | conduktor-provisioner containers' Security Context                                                                   | `{}`                        |

### State management configuration

Configuration for CLI provisioner state persistence of manged resources.
Enabled by default, it allows provisioner to track the resources it has created and manage them properly.

| Name                           | Description                                            | Value                  |
| ------------------------------ | ------------------------------------------------------ | ---------------------- |
| `state.enabled`                | Enable state persistence                               | `true`                 |
| `state.backend`                | State backend type. Currently only "file" is supported | `file`                 |
| `state.file.mountPath`         | Mount path for the state volume                        | `/var/conduktor/state` |
| `state.file.pvc.existingClaim` | Name of an existing PersistentVolumeClaim to use       | `""`                   |
| `state.file.pvc.labels`        | Labels for the PersistentVolumeClaim                   | `{}`                   |
| `state.file.pvc.annotations`   | Annotations for the PersistentVolumeClaim              | `{}`                   |
| `state.file.pvc.storageClass`  | Storage class for the PersistentVolumeClaim            | `""`                   |
| `state.file.pvc.storageSize`   | Size of the PersistentVolumeClaim                      | `1Gi`                  |
| `state.file.pvc.accessModes`   | Access modes for the PersistentVolumeClaim             | `["ReadWriteOnce"]`    |
| `state.file.pvc.selector`      | Selector for the PersistentVolumeClaim                 | `{}`                   |

### Other Parameters

Other parameters for the provisioner job.

| Name                                          | Description                                                      | Value  |
| --------------------------------------------- | ---------------------------------------------------------------- | ------ |
| `serviceAccount.create`                       | Specifies whether a ServiceAccount should be created             | `true` |
| `serviceAccount.name`                         | The name of the ServiceAccount to use.                           | `""`   |
| `serviceAccount.annotations`                  | Additional Service Account annotations (evaluated as a template) | `{}`   |
| `serviceAccount.automountServiceAccountToken` | Automount service account token for the server service account   | `true` |

## Examples values

### Provision Console
You can provision Conduktor Console only by setting `console.enabled` to `true`.

```yaml
console:
  enabled: true
  url: "http://console"
  username:  "<user_email>"
  password: "<password>"
  # OR
  apiToken: "<api_token>"
  insecure: true
  # Embedded manifests to apply on the Console
  manifests:
    - apiVersion: iam/v2
      kind: User
      metadata:
        name: john.doe@company.org
      spec:
        firstName: "John"
        lastName: "Doe"
    - apiVersion: iam/v2
      kind: User
      metadata:
        name: bob@company.org
      spec:
        firstName: "Bob"
        lastName: "Smith"
    - apiVersion: iam/v2
      kind: Group
      metadata:
        name: developers-a
      spec:
        displayName: "Developers Team A"
        description: "Members of the Team A - Developers"
        externalGroups:
          - "LDAP-GRP-A-DEV"
        members:
          - john.doe@company.org
          - bob@company.org
```

> Note: Embedded manifests are stored into a configmap configured by `console.manifestsConfigMap` and `console.manifestsConfigMapKey`(default `00-console-resources.yaml`) parameters.

### Provision Gateway
You can provision Conduktor Gateway only by setting `gateway.enabled` to `true`.

```yaml
gateway:
  enabled: true
  url: "http://gateway"
  username: "<user_email>"
  password: "<password>"
  manifests:
    - apiVersion: gateway/v2
      kind: GatewayServiceAccount
      metadata:
        vCluster: passthrough
        name: user-sa
      spec:
        type: LOCAL
    - apiVersion: gateway/v2
      kind: VirtualCluster
      metadata:
        name: "my-app-A"
      spec:
        aclEnabled: false
        superUsers:
          - admin
```

> Note: Embedded manifests are stored into a configmap configured by `console.manifestsConfigMap` and `console.manifestsConfigMapKey`(default `00-gateway-resources.yaml`) parameters.

### Provision Console and Gateway
You can provision both Console and Gateway in the same Helm release by setting both `console.enabled` and `gateway.enabled` to `true`.

> Note: The provisioning will share the same Job but use different containers for Console and Gateway provisioning.
> And so there is no interdependency between the Console and Gateway provisioning.

```yaml
console:
    enabled: true
    url: "http://console"
    username: "<user_email>"
    password: "<password>"
    manifests: [] # Embedded manifests to apply on the Console
gateway:
    enabled: true
    url: "http://gateway"
    username: "<user_email>"
    password: "<password>"
    manifests: [] # Embedded manifests to apply on the Gateway
```

### Use secrets and configmaps for configuration
You can use a ConfigMap and a Secret to store the environment variables for the Console and Gateway provisioning.
This is useful for sensitive information like passwords or API tokens.
For details on supported environment variables, please refer to the [Conduktor CLI documentation](https://github.com/conduktor/ctl)

```yaml
console:
  enabled: true
  url: "http://console"
  #  username: "" Provided by extraEnvVarsCM
  #  password: "" Provided by extraEnvVarsSecret
  extraEnvVarsCM: "console-provisioner-config"
  extraEnvVarsSecret: "console-provisioner-secrets"

  manifests: [] # Embedded manifests to apply on the Console

# Deploy a ConfigMap and a Secret with CLI configuration environment variables
extraDeploy:
  - apiVersion: v1
    kind: ConfigMap
    metadata:
      name: console-provisioner-config
    data:
      CDK_USER: "test@test.io"
  - apiVersion: v1
    kind: Secret
    metadata:
      name: console-provisioner-secrets
    data:
      CDK_PASSWORD: dGVzdFA0c3Mh  # base64 of "testP4ss!"
```

### Provide manifests from a ConfigMap
You can also use a ConfigMap to provide the manifests to apply on the Console and Gateway provisioning.

```yaml
console:
  enabled: true
  url: "http://console"
  username: "<user_email>"
  password: "<password>"
  extraEnvVars:
    - name: EXTRA_USER_EMAIL
      value: "extra-user@company.org"
  extraManifestsConfigMapRef:
      - name: extra-manifests
        key: console-setup.yaml

gateway:
    enabled: true
    url: "http://gateway"
    username: "<user_email>"
    password: "<password>"
    extraManifestsConfigMapRef:
      - name: extra-manifests
        key: gateway-setup.yaml

extraDeploy:
  - apiVersion: v1
    kind: ConfigMap
    metadata:
      name: extra-manifests
    data:
      console-setup.yaml: |
        apiVersion: iam/v2
        kind: User
        metadata:
          name: "${EXTRA_USER_EMAIL}"
        spec:
          firstName: "${EXTRA_USER_FIRSTNAME:-Default Name}"
          lastName: "User"
      gateway-setup.yaml: |
        apiVersion: gateway/v2
        kind: GatewayServiceAccount
        metadata:
          vCluster: passthrough
          name: extra-user
        spec:
          type: LOCAL
```

> Note: The `${EXTRA_USER_EMAIL}` and `${EXTRA_USER_FIRSTNAME}` variables will be replaced container environment variables.
> In this case by the values provided in the `extraEnvVars` section for `EXTRA_USER_EMAIL` and default value "Default Name" for missing `EXTRA_USER_FIRSTNAME`.

### Using different CLI commands

You can use different CLI commands by overriding the default command and args of the conduktor-provisioner container.

```yaml
console:
  enabled: true
  url: "http://console"
  username: "<user_email>"
  password: "<password>"
  args: ["delete", "-f", "/conf"]
  manifests:
    - apiVersion: iam/v2
      kind: User
      metadata:
        name: john.doe@company.org
      spec:
        firstName: "John"
        lastName: "Doe"
```
Will delete the user `john.doe@company.org`.

### Using CronJob to run the provisioner
You can configure the provisioner to run as a [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/) by setting `cronJob.enabled` to `true` and a cron pattern in `cronJob.schedule`.

```yaml
cronJob:
  enabled: true
  schedule: "0 0 * * *" # Run daily at midnight
  timezone: "UTC" # Optional, set the timezone for the cron job

console:
  enabled: true
  url: "http://console"
  username:  "<user_email>"
  password: "<password>"
  # Embedded manifests to apply on the Console
  manifests: []
```

## Troubleshooting

### Immutable job error
If you encounter an error like `Job.batch "conduktor-provisioner" is invalid: spec.template: Invalid value: core.PodTemplateSpec{...}: field is immutable`, it means that the job already exists and you are trying to change its template.

By default, the provisioner job use [Helm hooks](https://helm.sh/docs/topics/charts_hooks/) (`useHooks: true`) to recreate the job on each Helm release upgrade.
Try to enable it or use custom annotations to force the job recreation on each upgrade.

```yaml
useHooks: true
# or
commonAnnotations:
  helm.sh/hook: pre-install,pre-upgrade
  helm.sh/hook-delete-policy: before-hook-creation
```

You can also manually delete the existing release and job using:

```shell
helm delete <release_name> --namespace <namespace>
kubectl delete job <release_name>-provisioner --namespace <namespace>
```

For guides and advanced help, please refer to our
[documentation](https://docs.conduktor.io/platform/installation/get-started/kubernetes),
or to our charts `README`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
