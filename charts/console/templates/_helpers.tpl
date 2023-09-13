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
{{- if .Values.platform.existingConfigmap -}}
    {{ include "common.tplvalues.render" (dict "value" .Values.platformCortex.existingConfigmap "context" $) }}
{{- else -}}
    {{ include "conduktor.platformCortex.fullname" . }}
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
    {{- printf "%s-%s" (include "common.names.fullname" .) "cortex" | trunc 63 | trimSuffix "-" -}}
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
Platform external url
*/}}
{{- define "conduktor.platform.externalUrl" -}}
{{- $proto := ternary "https" "http" .Values.ingress.tls -}}
{{- printf "%s://%s" $proto .Values.ingress.hostname -}}
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
{{- with .Values.config.monitoring.storage }}
{{- if or (or .s3 .gcs) (or .azure .swift) -}}
conduktor: invalid monitoring storage configuration
           config.monitoring.storage is deprecated, move to monitoringConfig.storage instead
{{- end -}}
{{- end -}}
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
{{- required (printf "\n\nYOUR DEPLOYMENT WILL NOT WORK:\n\n%s" $message) .Values.unknown -}}
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
Return platform monitoring cortex url. Like http://cortex.nsp.svc.cluster.local:9009/
*/}}
{{- define "conduktor.monitoring.cortexUrl" -}}
{{- $url := printf "http://%s:%d/" (include "conduktor.platformCortex.serviceDomain" .) (.Values.platformCortex.service.ports.cortex | int) -}}
{{- if .Values.config.monitoring -}}
{{- $url := (default $url (index .Values "config" "monitoring" "cortex-url")) }}
{{- end -}}
{{- printf "%s" $url -}}
{{- end -}}

{{/*
Return platform monitoring alertmanager url. Like http://cortex.nsp.svc.cluster.local:9010/
*/}}
{{- define "conduktor.monitoring.alertManagerUrl" -}}
{{- $url := printf "http://%s:%d/" (include "conduktor.platformCortex.serviceDomain" .) (.Values.platformCortex.service.ports.alertmanager | int) -}}
{{- if .Values.config.monitoring -}}
{{- $url := (default $url (index .Values "config" "monitoring" "alert-manager-url")) }}
{{- end -}}
{{- printf "%s" $url -}}
{{- end -}}

{{/*
Return platform monitoring callback url. Like http://platform.nsp.svc.cluster.local:8080/monitoring/api/
This is used by alertmanager as a webhook to send alerts to the platform
*/}}
{{- define "conduktor.monitoring.callbackUrl" -}}
{{- $url := printf "http://%s:%d/monitoring/api/" (include "conduktor.platform.serviceDomain" .) (.Values.service.ports.http | int) -}}
{{- if .Values.config.monitoring -}}
{{- $url := (default $url (index .Values "config" "monitoring" "callback-url")) }}
{{- end -}}
{{- printf "%s" $url -}}
{{- end -}}

{{/*
Return platform monitoring notification callback url. Like http://conduktor.mydomain.com
This is used to return on the platform when a user click on a notification.
If ingress is not enabled, this will return the service internal url instead but notification link will not work.
*/}}
{{- define "conduktor.monitoring.notificationsCallbackUrl" -}}
{{- $ingressUrl := (include "conduktor.platform.externalUrl" .) -}}
{{- $serviceUrl := printf "http://%s:%d" (include "conduktor.platform.serviceDomain" .) (.Values.service.ports.http | int) -}}
{{- $url := ternary $ingressUrl $serviceUrl .Values.ingress.enabled  -}}
{{- if .Values.config.monitoring -}}
{{- $url := (default $url (index .Values "config" "monitoring" "notifications-callback-url")) }}
{{- end -}}
{{- printf "%s" $url -}}
{{- end -}}


{{/*
Return platform internal url. Like http://platform.nsp.svc.cluster.local:8080
*/}}
{{- define "conduktor.monitoring.consoleUrl" -}}
{{- $url := printf "%s:%d" (include "conduktor.platform.serviceDomain" .) (.Values.service.ports.http | int) -}}
{{- if .Values.monitoringConfig -}}
{{- $url := (default $url (index .Values "monitoringConfig" "console-url")) }}
{{- end -}}
{{- printf "%s" $url -}}
{{- end -}}
