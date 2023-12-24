{{/*
Return the proper platform image name
*/}}
{{- define "conduktor.image" -}}
{{ include "common.images.image" (dict "imageRoot" .Values.platform.image "global" .Values.global) }}
{{- end -}}

{{/*
Return the proper platform cortex image name
*/}}
{{- define "conduktor.cortex.image" -}}
{{ include "common.images.image" (dict "imageRoot" .Values.platformCortex.image "global" .Values.global) }}
{{- end -}}

{{/*
Return the proper Docker Image Registry Secret Names
*/}}
{{- define "conduktor.imagePullSecrets" -}}
{{- include "common.images.renderPullSecrets" (dict "images" (list .Values.platform.image .Values.platformCortex.image) "global" .Values.global "context" $) -}}
{{- end -}}

{{/*
Return the full configuration for the platform ConfigMap

"$_" is needed as it prevent the output of the function to be printed in the template
*/}}
{{- define "conduktor.platform.config" -}}
{{- $config := .Values.config | deepCopy -}}
{{/* Delete sensitive data from ConfigMap */}}
{{- $_ := unset $config "organization" -}}
{{- $_ := unset $config "admin" -}}
{{- $_ := unset $config "license" -}}
{{- $_ := unset $config "existingLicenseSecret" -}}

{{- $platform := .Values.config.platform | deepCopy -}}
  {{- if empty .Values.config.platform.external.url -}}
        {{- $_ := unset $platform "external" -}}
  {{- end -}}
{{- $_ := unset $platform "https" -}}
{{- $_ := set $config "platform" $platform -}}

{{/* Delete database password/username from ConfigMap */}}
{{- $database := .Values.config.database | deepCopy -}}
{{- $_ := unset $database "password" -}}
{{- $_ := unset $database "username" -}}
{{- $_ := set $config "database" $database -}}

{{ include "common.tplvalues.render" (dict "value" $config "context" $) }}
{{- end -}}

{{/*
Return the proper Condutkor Platform fullname
*/}}
{{- define "conduktor.platform.fullname" -}}
{{- printf "%s-%s" (include "common.names.fullname" .) "platform" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Return the proper Condutkor Platform Cortex fullname
*/}}
{{- define "conduktor.platformCortex.fullname" -}}
{{- printf "%s-%s" (include "common.names.fullname" .) "cortex" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Return the TLS secret name for the platform pod
*/}}
{{- define "conduktor.platform.tls.secretName" -}}
{{- if .Values.config.platform.https.existingSecret }}
    {{- .Values.config.platform.https.existingSecret }}
{{- else }}
    {{- printf "%s-tls" (include "conduktor.platform.fullname" .) }}
{{- end }}
{{- end -}}

{{/*
Return true if platform TLS is enabled
*/}}
{{- define "conduktor.platform.tls.enabled" -}}
{{- if (.Values.config.platform.https).selfSigned -}}
  {{/* Auto signed TLS */}}
  {{- "1" -}}
{{- else if not (empty (.Values.config.platform.https).existingSecret) -}}
  {{/* TLS from secrets */}}
  {{- "1" -}}
{{- else if and ((.Values.config.platform.https).cert).path ((.Values.config.platform.https).key).path -}}
  {{/* TLS from plain text values */}}
  {{- "1" -}}
{{- else -}}
{{- "" }}
{{- end -}}
{{- end -}}

{{/*
Name of the platform ConfigMap
*/}}
{{- define "conduktor.platform.configMapName" -}}
{{- if .Values.platform.existingConfigmap -}}
    {{ include "common.tplvalues.render" (dict "value" .Values.platform.existingConfigmap "context" $) }}
{{- else -}}
    {{ include "conduktor.platform.fullname" . }}
{{- end -}}
{{- end -}}

{{/*
Name of the platform Cortex ConfigMap
*/}}
{{- define "conduktor.platformCortex.configMapName" -}}
{{- if .Values.platformCortex.existingConfigmap -}}
    {{ include "common.tplvalues.render" (dict "value" .Values.platformCortex.existingConfigmap "context" $) }}
{{- else -}}
    {{ include "conduktor.platformCortex.fullname" . }}
{{- end -}}
{{- end -}}

{{/*
Name of the platform grafana dashboard ConfigMap
*/}}
{{- define "conduktor.platform.dashboard.name" -}}
    {{- printf "%s-%s" (include "common.names.fullname" .) "dashboards" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Name of the platform grafana dashboard ConfigMap
*/}}
{{- define "conduktor.platform.dashboard.namespace" -}}
  {{- if not (empty .Values.platform.metrics.grafana.namespace) -}}
    {{- .Values.platform.metrics.grafana.namespace -}}
  {{- else -}}
    {{- include "common.names.namespace" . -}}
  {{- end -}}
{{- end -}}

{{/*
Name of the platform secret
*/}}
{{- define "conduktor.platform.secretName" -}}
    {{- if .Values.config.existingSecret -}}
    {{- .Values.config.existingSecret -}}
    {{- else -}}
    {{- printf "%s-%s" (include "common.names.fullname" .) "platform" | trunc 63 | trimSuffix "-" -}}
    {{- end -}}
{{- end -}}

{{/*
Name of the platform cortex secret
*/}}
{{- define "conduktor.platformCortex.secretName" -}}
    {{- if .Values.monitoringConfig.existingSecret -}}
    {{- .Values.monitoringConfig.existingSecret -}}
    {{- else -}}
    {{- printf "%s-%s" (include "common.names.fullname" .) "cortex" | trunc 63 | trimSuffix "-" -}}
    {{- end -}}
{{- end -}}

{{/*
Default name for the conduktor license secret
*/}}
{{- define "conduktor.license.secretNameDefault" -}}
{{- printf "%s-%s" (include "common.names.fullname" .) "license" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Name of the conduktor license
*/}}
{{- define "conduktor.license.secretName" -}}
{{- if .Values.config.existingLicenseSecret -}}
    {{ include "common.tplvalues.render" (dict "value" .Values.config.existingLicenseSecret "context" $) }}
{{- else -}}
    {{ include "conduktor.license.secretNameDefault" . }}
{{- end -}}
{{- end -}}

{{/*
Name of the platform Prometheus ServiceMonitor
*/}}
{{- define "conduktor.platform.serviceMonitorName" -}}
{{- printf "%s-%s" (include "common.names.fullname" .) "monitor" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Name of the platform Service
*/}}
{{- define "conduktor.platform.serviceName" -}}
    {{ include "common.names.fullname" . }}
{{- end -}}

{{/*
Platform service internal domain name
*/}}
{{- define "conduktor.platform.serviceDomain" -}}
{{- printf "%s.%s.svc.%s" (include "conduktor.platform.serviceName" .) .Release.Namespace .Values.clusterDomain -}}
{{- end -}}


{{/*
Platform internal url from service in format http(s)://platform.nsp.svc.cluster.local:8080
*/}}
{{- define "conduktor.platform.internalUrl" -}}
{{- $isSSLEnabled := not (empty (include "conduktor.platform.tls.enabled" .)) }}
{{- $proto := ternary "https" "http" $isSSLEnabled -}}
{{- printf "%s://%s:%d" $proto (include "conduktor.platform.serviceDomain" .) (.Values.service.ports.http | int) -}}
{{- end -}}


{{/*
Platform external url. Fallback to internal one if no external url configured or ingress is not enabled
*/}}
{{- define "conduktor.platform.externalUrl" -}}
{{- if .Values.config.platform.external.url -}}
{{- .Values.config.platform.external.url -}}
{{- else if .Values.ingress.enabled -}}
{{- $isSSLEnabled := not (empty (include "conduktor.platform.tls.enabled" .)) }}
{{- $proto := ternary "https" "http" (or .Values.ingress.tls $isSSLEnabled) -}}
{{- printf "%s://%s" $proto .Values.ingress.hostname -}}
{{- else -}}
{{- include "conduktor.platform.internalUrl" . -}}
{{- end -}}
{{- end -}}


{{/*
Name of the platform cortex Service
*/}}
{{- define "conduktor.platformCortex.serviceName" -}}
    {{ include "conduktor.platformCortex.fullname" . }}
{{- end -}}

{{/*
Platform Cortex service internal domain name
*/}}
{{- define "conduktor.platformCortex.serviceDomain" -}}
{{- printf "%s.%s.svc.%s" (include "conduktor.platformCortex.serviceName" .) .Release.Namespace .Values.clusterDomain -}}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "conduktor.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "common.names.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Return true if cert-manager required annotations for TLS signed certificates are set in the Ingress annotations
Ref: https://cert-manager.io/docs/usage/ingress/#supported-annotations
*/}}
{{- define "conduktor.ingress.certManagerRequest" -}}
{{ if or (hasKey . "cert-manager.io/cluster-issuer") (hasKey . "cert-manager.io/issuer") }}
    {{- true -}}
{{- end -}}
{{- end -}}

{{- define "conduktor.validateValues.database" -}}
{{- if not .Values.config.existingSecret -}}
    {{- if not .Values.config.database.host -}}
conduktor: invalid database configuration
           config.database.host MUST be set in values
    {{- else if not .Values.config.database.name -}}
conduktor: invalid database configuration
           config.database.name MUST be set in values
    {{- end -}}
{{- end -}}
{{- end -}}

{{- define "conduktor.validateValues.monitoring" -}}
{{- if (.Values.config.monitoring).storage -}}
conduktor: invalid monitoring storage configuration
           config.monitoring.storage is deprecated, move to monitoringConfig.storage instead
{{- end -}}
{{- end -}}

{{/*
Compile all warnings into a single message.

Those are warnings and not errors, they are only output in NOTES.txt
*/}}
{{- define "conduktor.validateValues" -}}
{{- $messages := list -}}
{{- $messages := append $messages (include "conduktor.validateValues.database" .) -}}
{{- $messages := append $messages (include "conduktor.validateValues.monitoring" .) -}}
{{- $messages := without $messages "" -}}
{{- $message := join "\n" $messages -}}

{{- if $message -}}
{{- fail (printf "\n\nYOUR DEPLOYMENT WILL NOT WORK:\n\n%s" $message) -}}
{{- end -}}
{{- end -}}


{{/*
Return platform monitoring api poll rate for clusters. Default to 60s
*/}}
{{- define "conduktor.monitoring.clustersRefreshInterval" -}}
{{- $refresh := "60" -}}
{{- if .Values.config.monitoring -}}
{{- $refresh := (default $refresh (index .Values "config" "monitoring" "clusters-refresh-interval")) }}
{{- end -}}
{{- printf "%s" $refresh -}}
{{- end -}}

{{/*
Return platform monitoring cortex url. Like http(s)://cortex.nsp.svc.cluster.local:9009/
*/}}
{{- define "conduktor.monitoring.cortexUrl" -}}
{{- $url := printf "http://%s:%d/" (include "conduktor.platformCortex.serviceDomain" .) (.Values.platformCortex.service.ports.cortex | int) -}}
{{- if .Values.config.monitoring -}}
{{- $url := (default $url (index .Values "config" "monitoring" "cortex-url")) }}
{{- end -}}
{{- printf "%s" $url -}}
{{- end -}}

{{/*
Return platform monitoring alertmanager url. Like http(s)://cortex.nsp.svc.cluster.local:9010/
*/}}
{{- define "conduktor.monitoring.alertManagerUrl" -}}
{{- $url := printf "http://%s:%d/" (include "conduktor.platformCortex.serviceDomain" .) (.Values.platformCortex.service.ports.alertmanager | int) -}}
{{- if .Values.config.monitoring -}}
{{- $url := (default $url (index .Values "config" "monitoring" "alert-manager-url")) }}
{{- end -}}
{{- printf "%s" $url -}}
{{- end -}}

{{/*
Return platform monitoring callback url. Like http(s)://platform.nsp.svc.cluster.local:8080/monitoring/api/
This is used by alertmanager as a webhook to send alerts to the platform
*/}}
{{- define "conduktor.monitoring.callbackUrl" -}}
{{- $url := printf "%v/monitoring/api/" (include "conduktor.platform.internalUrl" .)  -}}
{{- if .Values.config.monitoring -}}
{{- $url := (default $url (index .Values "config" "monitoring" "callback-url")) }}
{{- end -}}
{{- printf "%s" $url -}}
{{- end -}}

{{/*
Return platform monitoring notification callback url. Like http(s)://conduktor.mydomain.com
This is used to return on the platform when a user click on a notification.
If ingress is not enabled, this will return the service internal url instead but notification link will not work.
*/}}
{{- define "conduktor.monitoring.notificationsCallbackUrl" -}}
{{- $url := include "conduktor.platform.externalUrl" .  -}}
{{- if .Values.config.monitoring -}}
{{- $url := (default $url (index .Values "config" "monitoring" "notifications-callback-url")) }}
{{- end -}}
{{- printf "%s" $url -}}
{{- end -}}

{{/*
Return platform internal url. Like http(s)://platform.nsp.svc.cluster.local:8080
*/}}
{{- define "conduktor.monitoring.consoleUrl" -}}
{{- default (include "conduktor.platform.internalUrl" .) (index .Values "monitoringConfig" "console-url") }}
{{- end -}}

{{/*
  Path where platform CA cert file is mounted in the Cortex pod.
  Default to /etc/conduktor/platform-tls/ca.crt
*/}}
{{- define "conduktor.monitoring.caFile" -}}
{{- default "/etc/conduktor/platform-tls/ca.crt" ((.Values.monitoringConfig).scraper).caFile }}
{{- end -}}

{{/*
Return platform monitoring storage type configured. Default to filesystem.
*/}}
{{- define "conduktor.monitoring.storageType" -}}
{{- $storageType := "filesystem" -}}
{{- range $key, $val := .Values.monitoringConfig.storage -}}
  {{- if $key -}}
    {{- $storageType = $key -}}
  {{- end -}}
{{- end -}}
{{- printf "%s" $storageType -}}
{{- end -}}

{{/*
Return platform monitoring env value
Usage :
{{ include "conduktor.monitoring.envValue" (dict "name" "MY_ENV_NAME" "value" .Values.path.to.value) }}
*/}}
{{- define "conduktor.monitoring.envValue" -}}
  {{- if or .value (eq (.value | toString) "false") -}}
  {{ printf "%s: %s" .name (.value | quote) }}
  {{- end -}}
{{- end -}}

{{/*
Return platform monitoring env secret
Usage :
{{ include "conduktor.monitoring.envSecret" (dict "name" "MY_ENV_NAME" "value" .Values.path.to.value) }}
*/}}
{{- define "conduktor.monitoring.envSecret" -}}
  {{- if .value -}}
  {{ printf "%s: %s" .name (.value | b64enc) }}
  {{- end -}}
{{- end -}}
