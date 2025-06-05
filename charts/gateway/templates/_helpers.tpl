{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "conduktor-gateway.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "conduktor-gateway.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create default secret name
*/}}
{{- define "conduktor-gateway.default.secretName" -}}
{{- printf "%s-secret" (include "conduktor-gateway.fullname" . | trunc 63 | trimSuffix "-") -}}
{{- end -}}


{{/*
Create default secret name
*/}}
{{- define "conduktor-gateway.secretName" -}}
  {{- if .Values.gateway.secretRef -}}
    {{- .Values.gateway.secretRef -}}
  {{- else -}}
    {{- include "conduktor-gateway.default.secretName" . -}}
  {{- end -}}
{{- end -}}


{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "conduktor-gateway.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "conduktor-gateway.labels" -}}
{{- /* Delegate to common.labels.standard for Kubernetes standard labels */ -}}
{{ include "common.labels.standard" (dict "customLabels" .Values.commonLabels "context" $) }}
{{- end -}}

{{- define "conduktor-gateway.podSelectorLabels" -}}
app.kubernetes.io/name: {{ include "conduktor-gateway.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "conduktor-gateway.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "conduktor-gateway.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}


{{/*
Helper function that check if all env values are strings and warn if not
.*/}}
{{- define "conduktor-gateway.validate.env" -}}
  {{ $notStringEnv := list}}
  {{- range $key, $value := .Values.gateway.env }}
    {{- if ne (typeOf $value) "string" }}
      {{- $notStringEnv = append $notStringEnv $key }}
    {{- end }}
  {{- end }}
  {{- if $notStringEnv }}
    {{- fail (printf "Some gateway.env values are not typed as string : %v"  (join ", " $notStringEnv )) }}
  {{- end }}
{{- end -}}

{{/*
Helper function to check if KAFKA_BOOTSTRAP_SERVERS exists in either gateway.env or gateway.extraSecretEnvVars.
If it does not exist in either, or exists in both, fail the chart.
*/}}
{{- define "conduktor-gateway.validate.kafka-bootstrap-server" -}}
  {{- $env := .Values.gateway.env }}
  {{- $extraEnv := .Values.gateway.extraSecretEnvVars }}
  {{- $foundInEnv := hasKey $env "KAFKA_BOOTSTRAP_SERVERS" }}
  {{- $foundInExtraEnv := false }}
  {{- if $extraEnv }}
    {{- range $index, $item := $extraEnv }}
      {{- if eq (index $item "name") "KAFKA_BOOTSTRAP_SERVERS" }}
        {{- $foundInExtraEnv = true }}
      {{- end }}
    {{- end }}
  {{- end }}
  {{- if not (or $foundInEnv $foundInExtraEnv) }}
    {{- fail "KAFKA_BOOTSTRAP_SERVERS is not defined in either gateway.env or gateway.extraSecretEnvVars." }}
  {{- end }}
  {{- if and $foundInEnv $foundInExtraEnv }}
    {{- fail "KAFKA_BOOTSTRAP_SERVERS is defined in both gateway.env and gateway.extraSecretEnvVars, which is invalid." }}
  {{- end }}
{{- end -}}

{{- define "conduktor-gateway.internalServiceName" -}}
{{- printf "%s-internal" (include "conduktor-gateway.fullname" . | trunc 54) -}}
{{- end -}}

{{/*
Define external service name
*/}}
{{- define "conduktor-gateway.externalServiceName"}}
{{- printf "%s-external" (include "conduktor-gateway.fullname" . | trunc 54) -}}
{{- end -}}

{{/*
Namespace of the platform grafana dashboards
*/}}
{{- define "conduktor-gateway.dashboard.namespace" -}}
  {{- if not (empty .Values.metrics.grafana.namespace) -}}
    {{- .Values.metrics.grafana.namespace -}}
  {{- else -}}
    {{- include "common.names.namespace" . -}}
  {{- end -}}
{{- end -}}

{{/*
Generate default password for users if not defined and return a json of all users
*/}}
{{- define "conduktor-gateway.patchApiUsers" -}}
  {{- if .Values.gateway.admin.users -}}
    {{- range .Values.gateway.admin.users -}}
      {{- if empty .password -}}
       {{- $_ := set . "password" (randAlphaNum 20) -}}
      {{- end -}}
    {{- end -}}
    {{- toJson .Values.gateway.admin.users -}}
  {{- else -}}
    []
  {{- end -}}
{{- end -}}


{{/*
Get the first admin user from the list of users
*/}}
{{- define "conduktor-gateway.mainAdmin" -}}
  {{- $users := . -}}
  {{- $adminUser := dict -}}
  {{- if not (empty $users) -}}
    {{- range $user := $users -}}
      {{- if and (hasKey $user "admin") $user.admin -}}
        {{- if not $adminUser -}}
          {{- $adminUser = $user -}}
        {{- end -}}
      {{- end -}}
    {{- end -}}
  {{- end -}}
  {{- toJson $adminUser -}}
{{- end -}}


{{/*
Check if env exist in context
Usage : include "conduktor-gateway.envExists" (dict "envkey" "ENV_VAR_NAME" "context" $)
Params:
  - envKey - String - Required - Name of the env.
  - context - Context - Required - Parent context.
*/}}
{{- define "conduktor-gateway.envExists" -}}
  {{- $exists := false -}}
  {{- $exists = hasKey $.context.Values.gateway.env $.envkey -}}
  {{- if not $exists -}}
    {{- range $.context.Values.gateway.extraSecretEnvVars -}}
      {{- if eq .name $.envkey -}}
        {{- $exists = true -}}
      {{- end -}}
    {{- end -}}
  {{- end -}}
  {{- $exists -}}
{{- end -}}

{{/*
Return admin api scheme http or https
*/}}
{{- define "conduktor-gateway.adminAPIScheme" -}}
  {{- $scheme := "http" -}}
  {{- if eq (include "conduktor-gateway.envExists" (dict "envkey" "GATEWAY_HTTPS_KEY_STORE_PATH" "context" $)) "true"  -}}
    {{- $scheme = "https" -}}
  {{- end -}}
  {{- $scheme -}}
{{- end -}}


{{/*
Patch grafana dashboard inputs
Params :
  - dashboard - Dashboard object to patch inputs - Requred
  - context - Context - Required - Parent context.
*/}}
{{- define "conduktor-gateway.patchGrafanaDashboardInputs" -}}
  {{- $patchs := dict "INPUT_DS_PROMETHEUS" ($.context.Values.metrics.grafana.datasources.prometheus | default "prometheus") -}}
  {{- $patchs = merge $patchs (dict "INPUT_DS_LOKI" ($.context.Values.metrics.grafana.datasources.loki | default "loki")) -}}
  {{- $patchs = merge $patchs (dict "INPUT_GATEWAY_JOB_NAME" $.context.Release.Name) -}}

  {{- $patchs = merge $patchs (dict "datasource" ($.context.Values.metrics.grafana.datasources.prometheus | default "prometheus")) -}}
  {{- $patchs = merge $patchs (dict "loki_datasource" ($.context.Values.metrics.grafana.datasources.loki | default "loki")) -}}
  {{- $patchs = merge $patchs (dict "job" $.context.Release.Name) -}}

  {{/*  Patch inputs */}}
  {{- range $input_index, $input := $.dashboard.__inputs -}}
    {{- if hasKey $patchs $input.name -}}
      {{- $_ := set $input "value" (index $patchs $input.name) -}}
    {{- end -}}
  {{- end -}}


 {{- range $var_index, $variable := $.dashboard.templating.list -}}
    {{- if hasKey $patchs $variable.name -}}
      {{- $_ := set $variable "query" (index $patchs $variable.name) -}}
    {{- end -}}
  {{- end -}}

{{- end -}}