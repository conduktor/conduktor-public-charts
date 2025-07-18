<a name="readme-top" id="readme-top"></a>

# Conduktor Provisioner

> If you have any questions you can [submit feedback](https://support.conduktor.io/hc/en-gb/requests/new?ticket_form_id=17438365654417) or contact [support](https://www.conduktor.io/contact/support/).

## Introduction

Helm Chart to deploy Conduktor Provisioner on Kubernetes that will provision existing Conduktor products.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+


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
| `diagnosticMode.command` | Command to override all containers in the chart release                                 | `["sleep"]`     |
| `diagnosticMode.args`    | Args to override all containers in the chart release                                    | `["infinity"]`  |

### conduktor-ctl Parameters

| Name                            | Description                                                                                                                                              | Value                     |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| `image.registry`                | conduktor-ctl image registry                                                                                                                             | `REGISTRY_NAME`           |
| `image.repository`              | conduktor-ctl image repository                                                                                                                           | `conduktor/conduktor-ctl` |
| `image.digest`                  | conduktor-ctl image digest in the way sha256:aa.... Please note this parameter, if set, will override the tag image tag (immutable tags are recommended) | `""`                      |
| `image.pullPolicy`              | conduktor-ctl image pull policy                                                                                                                          | `IfNotPresent`            |
| `image.pullSecrets`             | conduktor-ctl image pull secrets                                                                                                                         | `[]`                      |
| `image.debug`                   | Enable conduktor-ctl image debug mode                                                                                                                    | `false`                   |
| `cleanupAfterFinished.enabled`  | Enable cleanup of Job after it's finished                                                                                                                | `false`                   |
| `cleanupAfterFinished.seconds`  | TTL to cleanup the Job after it's finished                                                                                                               | `600`                     |
| `restartPolicy`                 | Restart policy for conduktor-provisioner jobs                                                                                                            | `OnFailure`               |
| `backoffLimit`                  | Number of retries before the job is considered failed                                                                                                    | `10`                      |
| `podSecurityContext`            | conduktor-provisioner Pod Security Context                                                                                                               | `{}`                      |
| `podLabels`                     | Extra labels for conduktor-provisioner pods                                                                                                              | `{}`                      |
| `podAnnotations`                | Annotations for conduktor-provisioner pods                                                                                                               | `{}`                      |
| `podAffinityPreset`             | Pod affinity preset. Ignored if `affinity` is set. Allowed values: `soft` or `hard`                                                                      | `""`                      |
| `podAntiAffinityPreset`         | Pod anti-affinity preset. Ignored if `affinity` is set. Allowed values: `soft` or `hard`                                                                 | `soft`                    |
| `nodeAffinityPreset.type`       | Node affinity preset type. Ignored if `affinity` is set. Allowed values: `soft` or `hard`                                                                | `""`                      |
| `nodeAffinityPreset.key`        | Node label key to match. Ignored if `affinity` is set                                                                                                    | `""`                      |
| `nodeAffinityPreset.values`     | Node label values to match. Ignored if `affinity` is set                                                                                                 | `[]`                      |
| `priorityClassName`             | conduktor-provisioner pods' priorityClassName                                                                                                            | `""`                      |
| `affinity`                      | Affinity for conduktor-provisioner pods assignment                                                                                                       | `{}`                      |
| `nodeSelector`                  | Node labels for conduktor-provisioner pods assignment                                                                                                    | `{}`                      |
| `tolerations`                   | Tolerations for conduktor-provisioner pods assignment                                                                                                    | `[]`                      |
| `schedulerName`                 | Name of the k8s scheduler (other than default) for conduktor-provisioner pods                                                                            | `""`                      |
| `terminationGracePeriodSeconds` | Seconds conduktor-provisioner pods need to terminate gracefully                                                                                          | `""`                      |
| `topologySpreadConstraints`     | Topology Spread Constraints for conduktor-provisioner pod assignment spread across your cluster among failure-domains                                    | `[]`                      |
| `initContainers`                | List of init containers to add to the conduktor-provisioner job pod                                                                                      | `[]`                      |

### Init wait-for script configuration

| Name                        | Description                                                                                                                                              | Value             |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| `waitFor.image.registry`    | registry for wait-for curl image                                                                                                                         | `docker.io`       |
| `waitFor.image.repository`  | wait-for curl image repository                                                                                                                           | `curlimages/curl` |
| `waitFor.image.digest`      | wait-for curl image digest in the way sha256:aa.... Please note this parameter, if set, will override the tag image tag (immutable tags are recommended) | `""`              |
| `waitFor.image.pullPolicy`  | wait-for image pull policy                                                                                                                               | `IfNotPresent`    |
| `waitFor.image.pullSecrets` | wait-for image pull secrets                                                                                                                              | `[]`              |
| `waitFor.retries`           | Number of retries to wait for the service to be ready                                                                                                    | `10`              |
| `waitFor.retryInterval`     | Interval in seconds between retries                                                                                                                      | `5`               |

### Console provisioning configuration

| Name                                 | Description                                                                                                                  | Value                       |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| `console.enabled`                    | Enable Console provisioning                                                                                                  | `false`                     |
| `console.authMode`                   | Authentication mode on Console for Conduktor CLI, either "conduktor" or "external" if using API Gateway in front of Console. | `conduktor`                 |
| `console.url`                        | URL of the Console                                                                                                           | `""`                        |
| `console.username`                   | Username to authenticate on the Console                                                                                      | `""`                        |
| `console.password`                   | Password to authenticate on the Console                                                                                      | `""`                        |
| `console.apiToken`                   | API Token to authenticate on the Console                                                                                     | `""`                        |
| `console.caCert`                     | CA certificate of Console                                                                                                    | `""`                        |
| `console.insecure`                   | Skip TLS verification                                                                                                        | `false`                     |
| `console.debug`                      | Enable verbose debug mode                                                                                                    | `false`                     |
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
| `console.lifecycleHooks`             | for conduktor-provisioner containers to automate configuration before or after startup                                       | `{}`                        |
| `gateway.enabled`                    | Enable Gateway provisioning                                                                                                  | `true`                      |
| `gateway.url`                        | URL of the Gateway                                                                                                           | `""`                        |
| `gateway.username`                   | Username to authenticate on the Gateway                                                                                      | `""`                        |
| `gateway.password`                   | Password to authenticate on the Gateway                                                                                      | `""`                        |
| `gateway.apiToken`                   | API Token to authenticate on the Gateway                                                                                     | `""`                        |
| `gateway.caCert`                     | CA certificate of Gateway                                                                                                    | `""`                        |
| `gateway.insecure`                   | Skip TLS verification                                                                                                        | `false`                     |
| `gateway.debug`                      | Enable verbose debug mode                                                                                                    | `false`                     |
| `gateway.manifests`                  | Manifests YAML to apply on the Gateway                                                                                       | `[]`                        |
| `gateway.manifestsConfigMap`         | Manifests YAML to apply on the Gateway                                                                                       | `""`                        |
| `gateway.manifestsConfigMapKey`      | Manifests YAML to apply on the Gateway                                                                                       | `00-gateway-resources.yaml` |
| `gateway.extraManifestsConfigMapRef` | List of ConfigMaps references with extra manifests to apply on the Gateway                                                   | `[]`                        |
| `gateway.command`                    | Override default conduktor-provisioner container command (useful when using custom images)                                   | `["/bin/conduktor"]`        |
| `gateway.args`                       | Override default conduktor-provisioner container args (useful when using custom images)                                      | `["apply","-f","/conf"]`    |
| `gateway.extraEnvVars`               | Array with extra environment variables to add to conduktor-provisioner containers                                            | `[]`                        |
| `gateway.extraEnvVarsCM`             | Name of existing ConfigMap containing extra env vars for conduktor-provisioner containers                                    | `""`                        |
| `gateway.extraEnvVarsSecret`         | Name of existing Secret containing extra env vars for conduktor-provisioner containers                                       | `""`                        |
| `gateway.extraVolumes`               | Optionally specify extra list of additional volumes for the conduktor-provisioner pods                                       | `[]`                        |
| `gateway.extraVolumeMounts`          | Optionally specify extra list of additional volumeMounts for the conduktor-provisioner containers                            | `[]`                        |
| `gateway.resources.requests.cpu`     | CPU resource requests                                                                                                        | `100m`                      |
| `gateway.resources.requests.memory`  | Memory resource requests                                                                                                     | `50Mi`                      |
| `gateway.resources.limits.cpu`       | CPU limit for the platform container                                                                                         | `500m`                      |
| `gateway.resources.limits.memory`    | Memory limit for the container                                                                                               | `128Mi`                     |
| `gateway.containerSecurityContext`   | conduktor-provisioner containers' Security Context                                                                           | `{}`                        |
| `gateway.lifecycleHooks`             | for conduktor-provisioner containers to automate configuration before or after startup                                       | `{}`                        |

### Other Parameters

| Name                                          | Description                                                      | Value  |
| --------------------------------------------- | ---------------------------------------------------------------- | ------ |
| `serviceAccount.create`                       | Specifies whether a ServiceAccount should be created             | `true` |
| `serviceAccount.name`                         | The name of the ServiceAccount to use.                           | `""`   |
| `serviceAccount.annotations`                  | Additional Service Account annotations (evaluated as a template) | `{}`   |
| `serviceAccount.automountServiceAccountToken` | Automount service account token for the server service account   | `true` |

## Troubleshooting

For guides and advanced help, please refer to our
[documentation](https://docs.conduktor.io/platform/installation/get-started/kubernetes),
or to our charts `README`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
