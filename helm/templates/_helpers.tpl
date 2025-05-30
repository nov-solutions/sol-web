{{/*
Expand the name of the chart.
*/}}
{{- define "sol-web.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "sol-web.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "sol-web.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "sol-web.labels" -}}
helm.sh/chart: {{ include "sol-web.chart" . }}
{{ include "sol-web.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "sol-web.selectorLabels" -}}
app.kubernetes.io/name: {{ include "sol-web.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "sol-web.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "sol-web.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create PostgreSQL dependency values
*/}}
{{- define "sol-web.postgresql.fullname" -}}
{{- if .Values.postgresql.enabled }}
{{- printf "%s-postgresql" (include "sol-web.fullname" .) }}
{{- else }}
{{- .Values.postgresql.externalHost }}
{{- end }}
{{- end }}

{{- define "sol-web.postgresql.secretName" -}}
{{- if .Values.postgresql.enabled }}
{{- printf "%s-postgresql" (include "sol-web.fullname" .) }}
{{- else }}
{{- printf "%s-postgresql-external" (include "sol-web.fullname" .) }}
{{- end }}
{{- end }}

{{/*
Create Redis dependency values
*/}}
{{- define "sol-web.redis.fullname" -}}
{{- if .Values.redis.enabled }}
{{- printf "%s-redis" (include "sol-web.fullname" .) }}
{{- else }}
{{- .Values.redis.externalHost }}
{{- end }}
{{- end }}

{{- define "sol-web.redis.secretName" -}}
{{- if .Values.redis.enabled }}
{{- printf "%s-redis" (include "sol-web.fullname" .) }}
{{- else }}
{{- printf "%s-redis-external" (include "sol-web.fullname" .) }}
{{- end }}
{{- end }}
