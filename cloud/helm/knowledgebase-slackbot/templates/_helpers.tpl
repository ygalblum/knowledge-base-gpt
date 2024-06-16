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
Embedding DB Volume name
*/}}
{{- define "knowledgebase-slackbot.embedding-pvc" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "embedding" }}
{{- end }}

{{/*
Ingest Job name
*/}}
{{- define "knowledgebase-slackbot.ingest" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "ingest" }}
{{- end }}

{{/*
Slackbot Pod name
*/}}
{{- define "knowledgebase-slackbot.slackbot-pod-name" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "slackbot" }}
{{- end }}

{{/*
Redis Service name
*/}}
{{- define "knowledgebase-slackbot.redis-host" -}}
{{- printf "%s-redis-master" .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "knowledgebase-slackbot.redis-password-secret" -}}
{{- printf "%s-redis" .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Redis StatefulSet name
*/}}
{{- define "knowledgebase-slackbot.redis-statefulset-name" -}}
{{- printf "%s-redis-master" .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}


{{/*
Elasticsearch Service name
*/}}
{{- define "knowledgebase-slackbot.elasticsearch" -}}
{{- printf "%s-elasticsearch" .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Kibana Service name
*/}}
{{- define "knowledgebase-slackbot.kibana" -}}
{{- printf "%s-kibana" .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
MetricBeat Pod name
*/}}
{{- define "knowledgebase-slackbot.metricbeat-pod-name" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "metricbeat" }}
{{- end }}

{{/*
vLLM Cache Volume name
*/}}
{{- define "knowledgebase-slackbot.vllm-pvc" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "vllm-cache" }}
{{- end }}

{{/*
vLLM Deployment name
*/}}
{{- define "knowledgebase-slackbot.vllm-deployment-name" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "vllm" }}
{{- end }}

{{/*
vLLM Service name
*/}}
{{- define "knowledgebase-slackbot.vllm-service-name" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "vllm" }}
{{- end }}

{{/*
vLLM Endpoint
*/}}
{{- define "knowledgebase-slackbot.vllm-endpoint" -}}
{{- printf "http://%s:8000/v1" (include "knowledgebase-slackbot.vllm-service-name" .) }}
{{- end }}

{{/*
Redis PVC Name
*/}}
{{- define "knowledgebase-slackbot.redis-pvc-name" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "redis" }}
{{- end }}

{{/*
Helm Hooks ServiceAccount Name
*/}}
{{- define "knowledgebase-slackbot.helm-hooks-serviceaccount-name" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "helm-hooks" }}
{{- end }}

{{/*
Helm Hooks Role Name
*/}}
{{- define "knowledgebase-slackbot.helm-hooks-role-name" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "helm-hooks" }}
{{- end }}

{{/*
Helm Hooks RoleBinding Name
*/}}
{{- define "knowledgebase-slackbot.helm-hooks-rolebinding-name" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "helm-hooks" }}
{{- end }}

{{/*
Redis PVC Patcher Job Name
*/}}
{{- define "knowledgebase-slackbot.redis-patcher-job-name" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "redis-patcher" }}
{{- end }}

{{/*
Redis PVC Patcher Fix ConfigMap Name
*/}}
{{- define "knowledgebase-slackbot.redis-patcher-configmap-name" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "redis-patcher" }}
{{- end }}

{{/*
Ingest Job hook ConfigMap Name
*/}}
{{- define "knowledgebase-slackbot.ingest-job-hook-configmap-name" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "ingest-job-hook" }}
{{- end }}

{{/*
Ingest Job hook Job Name
*/}}
{{- define "knowledgebase-slackbot.ingest-job-hook-job-name" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "ingest-job-hook" }}
{{- end }}
