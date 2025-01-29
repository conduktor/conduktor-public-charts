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
{{- define "conduktor-gateway.secretName" -}}
{{- printf "%s-secret" (include "conduktor-gateway.fullname" . | trunc 63 | trimSuffix "-") -}}
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
Computes the kafka bootstrap server URL. Resolves to embedded kafka by default but can be
opt-out for a custom bootstrap server.
*/}}
{{- define "conduktor-gateway.kafka-bootstrap-server" -}}
{{-   if .Values.kafka.enabled -}}
{{-     printf "%s-kafka-controller-headless.%s.svc.%s:9092" .Release.Name .Release.Namespace (default "cluster.local" .Values.clusterDomain) -}}
{{-   else -}}
{{-     required "value .kafka.bootstrapServers is required" .Values.kafka.bootstrapServers -}}
{{-   end -}}
{{- end -}}

{{/*
Define internal service name
*/}}
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
