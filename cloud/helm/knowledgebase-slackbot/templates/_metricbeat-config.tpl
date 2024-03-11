{{/*
MetricBeat configuration ConfigMap Name
*/}}
{{- define "knowledgebase-slackbot.metricbeat-config-configmap" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "metricbeat" }}
{{- end }}

{{/*
MetricBeat Configuration
*/}}
{{- define "knowledgebase-slackbot.metricbeat-config" -}}
metricbeat.modules:
- module: envoyproxy
  metricsets: ["server"]
  period: 10s
  hosts: ["https://{{ .Values.ollamaServerAddress }}:{{ .Values.ollamaServerAdminSecurePort }}"]
  ssl:
    enabled: true
    certificate_authorities: /certificates/ca.crt
    certificate: /certificates/tls.crt
    key: /certificates/tls.key
- module: prometheus
  period: 10s
  metricsets: ["collector"]
  hosts: ["https://{{ .Values.ollamaServerAddress }}:{{ .Values.ollamaServerFluentBitSecurePort }}"]
  metrics_path: /metrics
  ssl:
    enabled: true
    certificate_authorities: /certificates/ca.crt
    certificate: /certificates/tls.crt
    key: /certificates/tls.key
output.elasticsearch:
  hosts: ["{{ include "knowledgebase-slackbot.elasticsearch" .}}:9200"]
{{- end }}
