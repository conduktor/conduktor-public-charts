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
Default persistent volume claim name for stateful provisioner
*/}}
{{- define "provisioner.stateful.pvcName" -}}
  {{- if .Values.state.file.pvc.existingClaim -}}
    {{- .Values.state.file.pvc.existingClaim -}}
  {{- else -}}
    {{- printf "%s-stateful-pvc" (include "provisioner.fullname" .) -}}
  {{- end }}
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

{{/*
Generate command for provisioner
Parameters:
  config - provisioner configuration
  context - helm chart context
*/}}
{{- define "provisioner.command" -}}
  {{- if .context.Values.diagnosticMode.enabled -}}
  {{- toJson .context.Values.diagnosticMode.command}}
  {{- else -}}
  {{- toJson .config.command -}}
  {{- end -}}
{{- end }}

{{/*
Generate arguments for console provisioner
Parameters:
  config - provisioner configuration
  context - helm chart context
Usage:
{{- $args := include "provisioner.args" (dict "config" .Values.gateway "context" $) | fromJsonArray }}
*/}}
{{- define "provisioner.args" -}}
  {{- $args := list -}}
  {{- if .context.Values.diagnosticMode.enabled -}}
    {{- $args = .context.Values.diagnosticMode.args -}}
  {{- else -}}
    {{- if .config.args -}}
      {{- $args = .config.args -}}
    {{- else -}}
      {{- if .config.extraManifestsConfigMapRef -}}
        {{- $args = (list "apply" "-f" "/conf") -}}
      {{- else -}}
        {{- $args = (list "apply" "-f" (printf "/conf/%s" .config.manifestsConfigMapKey)) -}}
      {{- end -}}
    {{- end -}}

    {{- if .config.debug -}}
      {{- $args = append $args "-v" -}}
    {{- end -}}
  {{- end -}}

{{- toJson $args -}}
{{- end -}}


{{/*
Generate environment variables for stateful provisioner
Parameters:
  prefix - prefix for the state file name
  context - helm chart context
*/}}
{{- define "provisioner.stateful.env" -}}
  {{- $fileName := printf "%s-state.json" .prefix -}}
  {{- $env := dict -}}
  {{- if .context.Values.state.enabled -}}
    {{- $env = merge $env (dict "CDK_STATE_ENABLED" "true") -}}
    {{- if eq .context.Values.state.backend "file" -}}
      {{- $filePath := printf "%s/%s" .context.Values.state.file.mountPath $fileName -}}
      {{- $env = merge $env (dict "CDK_STATE_FILE" $filePath) -}}
    {{- end -}}
  {{- end -}}
{{- range $key, $value := $env }}
- name: {{ $key }}
  value: "{{ $value }}"
{{- end -}}
{{- end -}}