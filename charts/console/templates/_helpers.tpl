{{/*
Return the proper platform image name
*/}}
{{- define "conduktor.image" -}}
{{ include "common.images.image" (dict "imageRoot" .Values.platform.image "global" .Values.global) }}
{{- end -}}

{{/*
Return the proper Docker Image Registry Secret Names
*/}}
{{- define "conduktor.imagePullSecrets" -}}
{{- include "common.images.pullSecrets" (dict "images" (list .Values.platform.image) "global" .Values.global) -}}
{{- end -}}

{{/*
Return the full configuration for the platform ConfigMap

"$_" is needed as it prevent the output of the function to be printed in the template
*/}}
{{- define "conduktor.platform.config" -}}
{{ $config := .Values.config | deepCopy }}
{{/* Delete sensitive data from ConfigMap */}}
{{ $_ := unset $config "organization" }}
{{ $_ := unset $config "admin" }}
{{ $_ := unset $config "license" }}
{{ $_ := unset $config "existingLicenseSecret" }}

{{ $platform := .Values.config.platform | deepCopy }}
{{ if empty .Values.config.platform.external.url }}
    {{ $_ := unset $platform "external" }}
{{ end }}
{{ $_ := unset $platform "https" }}
{{ $_ := set $config "platform" $platform }}

{{/* Delete database password/username from ConfigMap */}}
{{ $database := .Values.config.database | deepCopy }}
{{ $_ := unset $database "password" }}
{{ $_ := unset $database "username" }}
{{ $_ := set $config "database" $database }}

{{ include "common.tplvalues.render" (dict "value" $config "context" $) }}
{{- end -}}

{{/*
Return the proper Condutkor Platform fullname
*/}}
{{- define "conduktor.platform.fullname" -}}
{{- printf "%s-%s" (include "common.names.fullname" .) "platform" | trunc 63 | trimSuffix "-" -}}
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
Name of the platform secret
*/}}
{{- define "conduktor.platform.secretName" -}}
    {{- printf "%s-%s" (include "common.names.fullname" .) "platform" | trunc 63 | trimSuffix "-" -}}
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
{{- if not .Values.config.database.host -}}
conduktor: invalid database configuration
           config.database.host MUST be set in values
{{- else if not .Values.config.database.name -}}
conduktor: invalid database configuration
           config.database.name MUST be set in values
{{- end -}}
{{- end -}}

{{/*
Compile all warnings into a single message.

Those are warnings and not errors, they are only output in NOTES.txt
*/}}
{{- define "conduktor.validateValues" -}}
{{- $messages := list -}}
{{- $messages := append $messages (include "conduktor.validateValues.database" .) -}}
{{- $messages := without $messages "" -}}
{{- $message := join "\n" $messages -}}

{{- if $message -}}
{{-   printf "\n\nYOUR DEPLOYMENT MIGHT NOT WORK:\n\n%s" $message -}}
{{- end -}}
{{- end -}}

