{{/*
Expand the name of the chart.
*/}}
{{- define "knowledgebase-slackbot.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "knowledgebase-slackbot.fullname" -}}
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
{{- define "knowledgebase-slackbot.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "knowledgebase-slackbot.labels" -}}
helm.sh/chart: {{ include "knowledgebase-slackbot.chart" . }}
{{ include "knowledgebase-slackbot.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "knowledgebase-slackbot.selectorLabels" -}}
app.kubernetes.io/name: {{ include "knowledgebase-slackbot.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "knowledgebase-slackbot.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "knowledgebase-slackbot.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Proxy Certificate secret name
*/}}
{{- define "knowledgebase-slackbot.proxy-certificate-secret" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "certificate" }}
{{- end }}

{{/*
Embedding DB Volume name
*/}}
{{- define "knowledgebase-slackbot.embedding-pvc" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "embedding" }}
{{- end }}

{{/*
Fluent-Bit Configuration ConfigMap name
*/}}
{{- define "knowledgebase-slackbot.fluent-bit-config" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "fluent-bit-config" }}
{{- end }}

{{/*
Ingest Job name
*/}}
{{- define "knowledgebase-slackbot.ingest" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "ingest" }}
{{- end }}

{{/*
Service JSON secret name
*/}}
{{- define "knowledgebase-slackbot.service-json-secret" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "service-json" }}
{{- end }}

{{/*
Ingest Folder ID secret name
*/}}
{{- define "knowledgebase-slackbot.folder-id-secret" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "folder-id" }}
{{- end }}

{{/*
Metrics Volume name
*/}}
{{- define "knowledgebase-slackbot.metrics-pvc" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "metrics" }}
{{- end }}

{{/*
Metrics Service name
*/}}
{{- define "knowledgebase-slackbot.metrics-service" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "metrics" }}
{{- end }}

{{/*
Forward Channel secret name
*/}}
{{- define "knowledgebase-slackbot.forward-channel-secret" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "forward-channel" }}
{{- end }}

{{/*
Slack Tokens secret name
*/}}
{{- define "knowledgebase-slackbot.slackbot-tokens-secret" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "slackbot-tokens" }}
{{- end }}

{{/*
Slackbot Pod name
*/}}
{{- define "knowledgebase-slackbot.slackbot-pod-name" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "slackbot" }}
{{- end }}
