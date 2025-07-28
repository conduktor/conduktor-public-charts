{{/*
Expand the name of the chart.
*/}}
{{- define "provisioner.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "provisioner.fullname" -}}
{{- include "common.names.fullname" . }}
{{- end }}

{{/*
Default fully qualified manifest config map name
*/}}
{{- define "provisioner.manifests.configMapName" -}}
{{- include "common.names.fullname" . }}-manifests
{{- end }}

{{/*
Default fully qualified init-scipts config map name
*/}}
{{- define "provisioner.initScript.configMapName" -}}
{{- include "common.names.fullname" . }}-init-script
{{- end }}

{{/*
Default fully qualified secret name
*/}}
{{- define "provisioner.console.config.secrets" -}}
{{- include "common.names.fullname" . }}-console-config-secret
{{- end }}

{{/*
Default fully qualified secret name
*/}}
{{- define "provisioner.gateway.config.secrets" -}}
{{- include "common.names.fullname" . }}-gateway-config-secret
{{- end }}

{{/*
Return the proper Docker Image Registry Secret Names
*/}}
{{- define "provisioner.imagePullSecrets" -}}
{{ include "common.images.pullSecrets" (dict "images" (list .Values.image) "global" .Values.global) }}
{{- end -}}


{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "provisioner.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "provisioner.labels" -}}
{{- $podLabels := include "common.tplvalues.merge" ( dict "values" ( list .Values.podLabels .Values.commonLabels ) "context" . ) }}
{{- include "common.labels.standard" ( dict "customLabels" $podLabels "context" $ ) -}}

{{- end }}

{{/*
Selector labels
*/}}
{{- define "provisioner.selectorLabels" -}}
app.kubernetes.io/name: {{ include "provisioner.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "provisioner.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "provisioner.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
