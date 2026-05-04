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
  - title - Dashboard title to override - Requred
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

  {{/*  Patch variables */}}
 {{- range $var_index, $variable := $.dashboard.templating.list -}}
    {{- if hasKey $patchs $variable.name -}}
      {{- $_ := set $variable "query" (index $patchs $variable.name) -}}

      {{/*  Update current value */}}
      {{- if hasKey $variable "current" -}}
        {{- $current := $variable.current | deepCopy -}}
        {{- $_newCurrent := set $current "value" (index $patchs $variable.name) -}}
        {{- $_2 := set $variable "current" $current -}}
      {{- end -}}
    {{- end -}}
  {{- end -}}

  {{/*  Patch title */}}
  {{- $_ := set $.dashboard "title" $.title -}}

{{- end -}}


{{- define "conduktor-gateway.nodeAffinity" -}}
{{- if .Values.affinity.nodeAffinity }}
{{- include "common.tplvalues.render" (dict "value" .Values.affinity.nodeAffinity "context" $) }}
{{- end -}}
{{- end -}}

{{- define "conduktor-gateway.podAffinity" -}}
{{- if .Values.affinity.podAffinity }}
{{- include "common.tplvalues.render" (dict "value" .Values.affinity.podAffinity "context" $) }}
{{- end -}}
{{- end -}}

{{- define "conduktor-gateway.podAntiAffinity" -}}
{{- if .Values.affinity.podAntiAffinity }}
{{- include "common.tplvalues.render" (dict "value" .Values.affinity.podAntiAffinity "context" $) }}
{{- else if and .Values.affinity.podAntiAffinityPreset .Values.affinity.podAntiAffinityPreset.enable -}}
preferredDuringSchedulingIgnoredDuringExecution:
  - podAffinityTerm:
      topologyKey: {{ .Values.affinity.podAntiAffinityPreset.topologyKey | default "kubernetes.io/hostname" | quote }}
      labelSelector:
        matchLabels:
          {{- include "conduktor-gateway.podSelectorLabels" . | nindent 10 }}
    weight: 1
{{- end -}}
{{- end -}}

{{/*
Unified port resolution: expand a list of port specs into a JSON object.
Input (.): list of port specs — "9092", "9092-9098", "443:9092", "443-445:9092-9094"
Output: JSON {"pairs": [{"advertised": N, "local": M}, ...]}
*/}}
{{- define "conduktor-gateway.portPairsJson" -}}
{{- $pairs := list -}}
{{- range . -}}
  {{- $spec := toString . -}}
  {{- $advPart := $spec -}}
  {{- $locPart := $spec -}}
  {{- if contains ":" $spec -}}
    {{- $parts := splitList ":" $spec -}}
    {{- $advPart = index $parts 0 -}}
    {{- $locPart = index $parts 1 -}}
  {{- end -}}
  {{- $advStart := int $advPart -}}
  {{- $advEnd := int $advPart -}}
  {{- if contains "-" $advPart -}}
    {{- $r := splitList "-" $advPart -}}
    {{- $advStart = int (index $r 0) -}}
    {{- $advEnd = int (index $r 1) -}}
  {{- end -}}
  {{- $locStart := int $locPart -}}
  {{- if contains "-" $locPart -}}
    {{- $locStart = int (index (splitList "-" $locPart) 0) -}}
  {{- end -}}
  {{- $count := int (add 1 (sub $advEnd $advStart)) -}}
  {{- range $i := untilStep 0 $count 1 -}}
    {{- $pairs = append $pairs (dict "advertised" (int (add $advStart $i)) "local" (int (add $locStart $i))) -}}
  {{- end -}}
{{- end -}}
{{- dict "pairs" $pairs | toJson -}}
{{- end -}}

{{/*
Expand a list of broker ID specs into a JSON list of integers.
Input (.): list of strings — "0", "0-2", "0-2,10,12-13"
Output: JSON {"ids": [0, 1, 2, 10, 12, 13]}
*/}}
{{- define "conduktor-gateway.expandBrokerIds" -}}
{{- $ids := list -}}
{{- range . -}}
  {{- range (splitList "," (toString .)) -}}
    {{- $part := trim . -}}
    {{- if contains "-" $part -}}
      {{- $bounds := splitList "-" $part -}}
      {{- $start := int (index $bounds 0) -}}
      {{- $end := int (index $bounds 1) -}}
      {{- range untilStep $start (add $end 1 | int) 1 -}}
        {{- $ids = append $ids . -}}
      {{- end -}}
    {{- else -}}
      {{- $ids = append $ids (int $part) -}}
    {{- end -}}
  {{- end -}}
{{- end -}}
{{- dict "ids" $ids | toJson -}}
{{- end -}}

{{/*
Auto-generate the per-broker advertised host pattern for internal SNI routing.
Produces: {fullname}-broker-{{nodeId}}.{namespace}.svc.{clusterDomain}
{{nodeId}} is kept as a literal string for Gateway to resolve at runtime.
*/}}
{{- define "conduktor-gateway.internalSNIAdvertisedHostPattern" -}}
{{- printf "%s-broker-{{nodeId}}.%s.svc.%s" (include "conduktor-gateway.fullname" . | trunc 50 | trimSuffix "-") .Release.Namespace .Values.clusterDomain -}}
{{- end -}}

{{/*
Return the first advertised port number from a single port spec string.
Input (.): one port spec string e.g. "9092-9098" or "443:9092"
Output: the first advertised port as a string e.g. "9092" or "443"
*/}}
{{- define "conduktor-gateway.firstAdvertisedPort" -}}
{{- $spec := toString . -}}
{{- $advPart := $spec -}}
{{- if contains ":" $spec -}}
  {{- $advPart = index (splitList ":" $spec) 0 -}}
{{- end -}}
{{- index (splitList "-" $advPart) 0 -}}
{{- end -}}

{{/*
Resolve the advertised host for the internal listener.
Defaults to the full FQDN of the *-internal service for cross-namespace reachability.
*/}}
{{- define "conduktor-gateway.internalListenerAdvertisedHost" -}}
{{- printf "%s.%s.svc.%s" (include "conduktor-gateway.internalServiceName" .) .Release.Namespace .Values.clusterDomain -}}
{{- end -}}

{{/*
Resolve the effective security mode.
Prefers gateway.env.GATEWAY_SECURITY_MODE if set, otherwise falls back to gateway.securityMode.
*/}}
{{- define "conduktor-gateway.resolveSecurityMode" -}}
{{- if hasKey .Values.gateway.env "GATEWAY_SECURITY_MODE" -}}
  {{- index .Values.gateway.env "GATEWAY_SECURITY_MODE" -}}
{{- else -}}
  {{- .Values.gateway.securityMode | default "GATEWAY_MANAGED" -}}
{{- end -}}
{{- end -}}

{{/*
Resolve the effective ACL enabled setting.
Priority: gateway.env.GATEWAY_ACL_ENABLED > gateway.aclEnabled > inferred from securityMode.
*/}}
{{- define "conduktor-gateway.resolveAclEnabled" -}}
{{- if hasKey .Values.gateway.env "GATEWAY_ACL_ENABLED" -}}
  {{- index .Values.gateway.env "GATEWAY_ACL_ENABLED" -}}
{{- else if not (empty (.Values.gateway.aclEnabled | toString)) -}}
  {{- .Values.gateway.aclEnabled | toString -}}
{{- else -}}
  {{- $securityMode := include "conduktor-gateway.resolveSecurityMode" . -}}
  {{- ternary "true" "false" (eq $securityMode "GATEWAY_MANAGED") -}}
{{- end -}}
{{- end -}}

{{/*
Generate env vars for listener mode (gateway.preview.listeners: true).
Returns a JSON object mapping env var names to string values.
Go template iterates JSON object keys in sorted order — output is deterministic.
*/}}
{{- define "conduktor-gateway.listenerModeEnvVars" -}}
{{- $securityMode := include "conduktor-gateway.resolveSecurityMode" . -}}
{{- $aclEnabled := include "conduktor-gateway.resolveAclEnabled" . -}}
{{- $vars := dict -}}
{{- $listenerNames := ternary "INTERNAL,EXTERNAL" "INTERNAL" .Values.service.external.enable -}}
{{- $_ := set $vars "GATEWAY_LISTENER_NAMES" $listenerNames -}}
{{- $_ := set $vars "GATEWAY_SECURITY_MODE" $securityMode -}}
{{- $_ := set $vars "GATEWAY_ACL_ENABLED" $aclEnabled -}}
{{- $_ := set $vars "GATEWAY_LISTENER_INTERNAL_SECURITY_PROTOCOL" .Values.gateway.listeners.internal.securityProtocol -}}
{{- $_ := set $vars "GATEWAY_LISTENER_INTERNAL_ROUTING" (.Values.gateway.listeners.internal.routing | upper) -}}
{{- $_ := set $vars "GATEWAY_LISTENER_INTERNAL_PORTS" (.Values.gateway.listeners.internal.ports | join ",") -}}
{{- $_ := set $vars "GATEWAY_LISTENER_INTERNAL_HOST" (include "conduktor-gateway.internalListenerAdvertisedHost" .) -}}
{{- if eq .Values.gateway.listeners.internal.routing "sni" -}}
  {{- $_ := set $vars "GATEWAY_LISTENER_INTERNAL_ADVERTISED_HOST_PATTERN" (include "conduktor-gateway.internalSNIAdvertisedHostPattern" .) -}}
  {{- $_ := set $vars "GATEWAY_LISTENER_INTERNAL_BOOTSTRAP_HOST_PATTERN" (include "conduktor-gateway.internalListenerAdvertisedHost" .) -}}
{{- end -}}
{{- if and .Values.gateway.listeners.internal.sslClientAuth (has .Values.gateway.listeners.internal.securityProtocol (list "SSL" "SASL_SSL")) -}}
  {{- $_ := set $vars "GATEWAY_LISTENER_INTERNAL_SSL_CLIENT_AUTH" .Values.gateway.listeners.internal.sslClientAuth -}}
{{- end -}}
{{- if .Values.service.external.enable -}}
  {{- $_ := set $vars "GATEWAY_LISTENER_EXTERNAL_SECURITY_PROTOCOL" .Values.gateway.listeners.external.securityProtocol -}}
  {{- $_ := set $vars "GATEWAY_LISTENER_EXTERNAL_ROUTING" (.Values.gateway.listeners.external.routing | upper) -}}
  {{- $_ := set $vars "GATEWAY_LISTENER_EXTERNAL_PORTS" (.Values.gateway.listeners.external.ports | join ",") -}}
  {{- $_ := set $vars "GATEWAY_LISTENER_EXTERNAL_HOST" .Values.gateway.listeners.external.advertisedHost -}}
  {{- if .Values.gateway.listeners.external.advertisedHostPattern -}}
    {{- $_ := set $vars "GATEWAY_LISTENER_EXTERNAL_ADVERTISED_HOST_PATTERN" .Values.gateway.listeners.external.advertisedHostPattern -}}
  {{- end -}}
  {{- if .Values.gateway.listeners.external.bootstrapHostPattern -}}
    {{- $_ := set $vars "GATEWAY_LISTENER_EXTERNAL_BOOTSTRAP_HOST_PATTERN" .Values.gateway.listeners.external.bootstrapHostPattern -}}
  {{- end -}}
  {{- if and .Values.gateway.listeners.external.sslClientAuth (has .Values.gateway.listeners.external.securityProtocol (list "SSL" "SASL_SSL")) -}}
    {{- $_ := set $vars "GATEWAY_LISTENER_EXTERNAL_SSL_CLIENT_AUTH" .Values.gateway.listeners.external.sslClientAuth -}}
  {{- end -}}
{{- end -}}
{{- toJson $vars -}}
{{- end -}}

{{/*
Generate env vars for legacy mode (gateway.preview.listeners: false).
Returns a JSON object mapping env var names to string values.
*/}}
{{- define "conduktor-gateway.legacyModeEnvVars" -}}
{{- $vars := dict -}}
{{- if not (hasKey .Values.gateway.env "GATEWAY_ADVERTISED_HOST") -}}
  {{- $_ := set $vars "GATEWAY_ADVERTISED_HOST" (include "conduktor-gateway.internalServiceName" .) -}}
{{- end -}}
{{- $_ := set $vars "GATEWAY_PORT_START" (toString .Values.gateway.portRange.start) -}}
{{- $_ := set $vars "GATEWAY_PORT_COUNT" (toString .Values.gateway.portRange.count) -}}
{{- toJson $vars -}}
{{- end -}}

{{/*
Validate listener mode configuration. Called from NOTES.txt.
Only runs when gateway.preview.listeners is true.
Accumulates all errors and fails once with a combined message.
*/}}
{{- define "conduktor-gateway.validate.listeners" -}}
{{- if .Values.gateway.preview.listeners -}}

{{- $errors := list -}}
{{- $securityMode := include "conduktor-gateway.resolveSecurityMode" . -}}
{{- $aclEnabled := include "conduktor-gateway.resolveAclEnabled" . -}}

{{- /* securityMode required */ -}}
{{- if empty $securityMode -}}
  {{- $errors = append $errors "- gateway.securityMode is required when gateway.preview.listeners is true." -}}
{{- end -}}

{{- /* aclEnabled incompatible with KAFKA_MANAGED */ -}}
{{- if and (eq $aclEnabled "true") (eq $securityMode "KAFKA_MANAGED") -}}
  {{- $errors = append $errors "- gateway.aclEnabled cannot be true when securityMode is KAFKA_MANAGED — ACL is a GATEWAY_MANAGED feature." -}}
{{- end -}}

{{- /* aclEnabled requires at least one authenticating listener */ -}}
{{- if eq $aclEnabled "true" -}}
  {{- $saslProtocols := list "SASL_PLAINTEXT" "SASL_SSL" -}}
  {{- $hasAuthListener := false -}}
  {{- if has .Values.gateway.listeners.internal.securityProtocol $saslProtocols -}}
    {{- $hasAuthListener = true -}}
  {{- end -}}
  {{- if and .Values.service.external.enable (has .Values.gateway.listeners.external.securityProtocol $saslProtocols) -}}
    {{- $hasAuthListener = true -}}
  {{- end -}}
  {{- if and (eq .Values.gateway.listeners.internal.securityProtocol "SSL") (ne (.Values.gateway.listeners.internal.sslClientAuth | default "NONE") "NONE") -}}
    {{- $hasAuthListener = true -}}
  {{- end -}}
  {{- if and .Values.service.external.enable (eq .Values.gateway.listeners.external.securityProtocol "SSL") (ne (.Values.gateway.listeners.external.sslClientAuth | default "NONE") "NONE") -}}
    {{- $hasAuthListener = true -}}
  {{- end -}}
  {{- if not $hasAuthListener -}}
    {{- $errors = append $errors "- gateway.aclEnabled is true but no listener supports authentication (no SASL or mTLS SSL listener) — ACL cannot be enforced." -}}
  {{- end -}}
{{- end -}}

{{- /* External listener requires advertisedHost */ -}}
{{- if and .Values.service.external.enable (empty .Values.gateway.listeners.external.advertisedHost) -}}
  {{- $errors = append $errors "- gateway.listeners.external.advertisedHost is required when gateway.preview.listeners and service.external.enable are both true." -}}
{{- end -}}

{{- /* Internal SNI requires brokerIds */ -}}
{{- if and (eq .Values.gateway.listeners.internal.routing "sni") (empty .Values.gateway.listeners.internal.brokerIds) -}}
  {{- $errors = append $errors "- gateway.listeners.internal.brokerIds is required when gateway.listeners.internal.routing is sni. Use range syntax e.g. [\"0-2\"] or [\"0-2,10,12-13\"]." -}}
{{- end -}}
{{- /* Internal SNI requires TLS (SNI is a TLS feature) */ -}}
{{- if and (eq .Values.gateway.listeners.internal.routing "sni") (has .Values.gateway.listeners.internal.securityProtocol (list "PLAINTEXT" "SASL_PLAINTEXT")) -}}
  {{- $errors = append $errors "- gateway.listeners.internal.securityProtocol must be SSL or SASL_SSL when routing is sni (SNI requires TLS)." -}}
{{- end -}}

{{- /* External SNI requires advertisedHostPattern */ -}}
{{- if and .Values.service.external.enable (eq .Values.gateway.listeners.external.routing "sni") (empty .Values.gateway.listeners.external.advertisedHostPattern) -}}
  {{- $errors = append $errors "- gateway.listeners.external.advertisedHostPattern is required when gateway.listeners.external.routing is sni." -}}
{{- end -}}

{{- /* SNI: external advertisedHostPattern must contain {{nodeId}}; bootstrapHostPattern must not */ -}}
{{- if .Values.service.external.enable -}}
  {{- $ext := .Values.gateway.listeners.external -}}
  {{- if and (eq $ext.routing "sni") (not (empty $ext.advertisedHostPattern)) -}}
    {{- if not (contains "{{nodeId}}" $ext.advertisedHostPattern) -}}
      {{- $errors = append $errors "- gateway.listeners.external.advertisedHostPattern must contain {{nodeId}} for SNI per-broker routing." -}}
    {{- end -}}
  {{- end -}}
  {{- if and (not (empty $ext.bootstrapHostPattern)) (contains "{{nodeId}}" $ext.bootstrapHostPattern) -}}
    {{- $errors = append $errors "- gateway.listeners.external.bootstrapHostPattern must not contain {{nodeId}}." -}}
  {{- end -}}
{{- end -}}

{{- /* SNI routing requires exactly one port spec */ -}}
{{- range list "internal" "external" -}}
  {{- $listenerName := . -}}
  {{- $listener := index $.Values.gateway.listeners $listenerName -}}
  {{- $isActive := or (eq $listenerName "internal") (and (eq $listenerName "external") $.Values.service.external.enable) -}}
  {{- if and $isActive (eq $listener.routing "sni") (gt (len $listener.ports) 1) -}}
    {{- $errors = append $errors (printf "- gateway.listeners.%s.ports must contain exactly one entry when routing is sni." $listenerName) -}}
  {{- end -}}
{{- end -}}

{{- /* TLS required for any SSL/SASL_SSL listener */ -}}
{{- $sslProtocols := list "SSL" "SASL_SSL" -}}
{{- if or (has .Values.gateway.listeners.internal.securityProtocol $sslProtocols)
          (and .Values.service.external.enable (has .Values.gateway.listeners.external.securityProtocol $sslProtocols)) -}}
  {{- if not .Values.tls.enable -}}
    {{- $errors = append $errors "- tls.enable must be true when any listener uses SSL or SASL_SSL securityProtocol." -}}
  {{- end -}}
{{- end -}}

{{- /* KAFKA_MANAGED requires SASL on all active listeners */ -}}
{{- if eq $securityMode "KAFKA_MANAGED" -}}
  {{- $saslProtocols := list "SASL_PLAINTEXT" "SASL_SSL" -}}
  {{- if not (has .Values.gateway.listeners.internal.securityProtocol $saslProtocols) -}}
    {{- $errors = append $errors "- KAFKA_MANAGED requires SASL; gateway.listeners.internal.securityProtocol must be SASL_PLAINTEXT or SASL_SSL." -}}
  {{- end -}}
  {{- if and .Values.service.external.enable (not (has .Values.gateway.listeners.external.securityProtocol $saslProtocols)) -}}
    {{- $errors = append $errors "- KAFKA_MANAGED requires SASL; gateway.listeners.external.securityProtocol must be SASL_PLAINTEXT or SASL_SSL." -}}
  {{- end -}}
{{- end -}}

{{- /* Local port overlap check between INTERNAL and EXTERNAL */ -}}
{{- if .Values.service.external.enable -}}
  {{- $internalData := include "conduktor-gateway.portPairsJson" .Values.gateway.listeners.internal.ports | fromJson -}}
  {{- $externalData := include "conduktor-gateway.portPairsJson" .Values.gateway.listeners.external.ports | fromJson -}}
  {{- $seen := dict -}}
  {{- range $internalData.pairs -}}
    {{- $_ := set $seen (toString .local) "internal" -}}
  {{- end -}}
  {{- range $externalData.pairs -}}
    {{- if hasKey $seen (toString .local) -}}
      {{- $errors = append $errors (printf "- Local port %v is used by both INTERNAL and EXTERNAL listeners — port ranges must not overlap." .local) -}}
    {{- end -}}
  {{- end -}}
{{- end -}}

{{- if gt (len $errors) 0 -}}
  {{- fail (printf "gateway.preview.listeners validation errors:\n%s" (join "\n" $errors)) -}}
{{- end -}}

{{- end -}}
{{- end -}}
