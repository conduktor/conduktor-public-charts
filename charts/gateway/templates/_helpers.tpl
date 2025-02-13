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
Helper function to check if KAFKA_BOOTSTRAP_SERVERS exists in either gateway.env or gateway.extraSecretEnvVars.
If it does not exist in either, or exists in both, fail the chart.
*/}}
{{- define "conduktor-gateway.kafka-bootstrap-server" -}}
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

{{/*
print_kafka_bootstrap_servers: This template function is used to print the Kafka bootstrap servers.
Usage: {{ include "print_kafka_bootstrap_servers" . }}
*/}}
{{- define "print_kafka_bootstrap_servers" }}
{{- $servers := "" }}

{{- if .Values.gateway.extraSecretEnvVars }}
  {{- range .Values.gateway.extraSecretEnvVars }}
    {{- if eq .name "KAFKA_BOOTSTRAP_SERVERS" }}
      {{- $servers = .value }}
    {{- end }}
  {{- end }}
{{- else if .Values.gateway.env.KAFKA_BOOTSTRAP_SERVERS }}
  {{- $servers = .Values.gateway.env.KAFKA_BOOTSTRAP_SERVERS }}
{{- end }}

{{- if $servers }}
  {{- $serverList := split "," $servers }}
Kafka Bootstrap Servers:
  {{- range $serverList }}
  - {{ . | trim }}
  {{- end }}
{{- else }}
No Kafka Bootstrap Servers configured.
{{- end }}
{{- end }}

{{- define "conduktor-gateway.internalServiceName" -}}
{{- printf "%s-internal" (include "conduktor-gateway.fullname" . | trunc 54) -}}
{{- end -}}

{{/*
Define external service name
*/}}
{{- define "conduktor-gateway.externalServiceName"}}
{{- printf "%s-external" (include "conduktor-gateway.fullname" . | trunc 54) -}}
{{- end -}}
